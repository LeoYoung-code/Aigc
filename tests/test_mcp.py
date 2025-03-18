from mcp_servers.mcp_tcp_client import MCPClient
from common import common
from simple_term_menu import TerminalMenu

def tools_menu():
    with MCPClient() as mcp:
        tools = mcp.get_available_tools()
    menu_items = [
        {"label": str(tool.get("name", "Unknown")), "preview": str(tool.get("description", "No description available"))}
        for tool in tools
    ]
    selected_tools = preview_multiselect_menu(menu_items, "Tools menu", preview_title="Tool description")
    return [tool for tool in tools if tool["name"] in selected_tools] if selected_tools else None


from typing import Callable, Dict, List, Optional, Union



def preview_multiselect_menu(
    items: List[Dict[str, str]],
    menu_title: str,
    skip_option: bool = False,
    show_search: bool = False,
    preview_size: float = 0.25,
    preview_title: str = "Preview",
    exit: bool = False,
    exit_message: str = "Goodbye! See you later!",
) -> Union[List[str], None]:
    """
    Creates a menu where items can be selected/unselected and each item has a preview text.
    Uses simple-term-menu for both multi-selection and preview.
    """
    labels = []
    previews = {}
    for item in items:
        label = item["label"]
        labels.append(label)
        previews[label] = item["preview"]

    if skip_option:
        labels.insert(0, "Skip")
        previews["Skip"] = "Skip this selection"

    if exit:
        labels.append("Exit")
        previews["Exit"] = "Exit the menu"

    # Function to generate preview text
    def preview_command(label: str) -> str:
        return previews.get(label, "")

    preselected = [label for label in labels if label not in ["Skip", "Exit"]]

    # Create TerminalMenu with preview
    terminal_menu = TerminalMenu(
        menu_entries=labels,
        title=menu_title,
        preview_command=preview_command,
        preview_size=preview_size,
        preview_title=preview_title,
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_cursor="[*] ",
        menu_cursor="» ",
        cycle_cursor=True,
        clear_screen=False,
        show_search_hint=show_search,
        preselected_entries=preselected,
        multi_select_empty_ok=True,
        multi_select_select_on_accept=False,
    )
    selected_indices = terminal_menu.show()

    if selected_indices is None:
        return None

    selected_labels = [labels[i] for i in selected_indices]

    if exit and "Exit" in selected_labels:
        return common.custom_print("exit", exit_message, 0)

    if skip_option and "Skip" in selected_labels:
        selected_labels.remove("Skip")

    return selected_labels if selected_labels else None

if __name__ == "__main__":
    tools_menu()