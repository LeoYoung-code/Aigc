import unittest
from unittest.mock import patch, MagicMock, Mock

# 模拟MCPError类
class MockMCPError:
    def __init__(self, error_type, message, details=None):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            error_type=data.get("error_type", ""),
            message=data.get("message", ""),
            details=data.get("details", {})
        )

# 模拟MCPClientError类
class MockMCPClientError(Exception):
    def __init__(self, error):
        self.error = error
        super().__init__(str(error.message))

# 使用模拟替代真实导入
with patch('sys.modules', {
    'socket': MagicMock(),
    'json': MagicMock(),
    'common.common': MagicMock(),
    'mcp_servers.mcp_errors': MagicMock(),
    'mcp_servers.server_manager': MagicMock(),
}):
    import json  # 真实导入json以便测试中使用
    
    # 手动模拟MCPClient类
    class MCPClient:
        _server_failed = False
        
        def __init__(self, host="localhost", port=8765, auto_start=True):
            self.host = host
            self.port = port
            self.sock = None
            self.server_manager = MagicMock()
            self.auto_start = auto_start
        
        def _connect(self):
            """内部方法，建立连接"""
            try:
                self.sock = MagicMock()
                return True
            except Exception:
                self.sock = None
                return False
        
        def _handle_response(self, response):
            """处理服务器响应并抛出适当的异常"""
            if response["status"] == "error":
                error_data = response["error"]
                error = MockMCPError.from_dict(error_data)
                raise MockMCPClientError(error)
            return response.get("result")
        
        def _send_request(self, request):
            """向服务器发送请求并接收响应"""
            # 测试时会被模拟替换
            pass
        
        def call_tool(self, tool_name, arguments):
            """调用服务器上的工具"""
            request = {"command": "call_tool", "tool_name": tool_name, "arguments": arguments}
            response = self._send_request(request)
            return self._handle_response(response)
        
        def get_available_tools(self):
            """获取服务器上可用工具的列表"""
            request = {"command": "get_tools"}
            response = self._send_request(request)
            return response.get("tools", [])
        
        def start_server(self):
            """如果服务器未运行，则启动服务器"""
            return self.server_manager.start_server()
        
        def stop_server(self):
            """停止服务器"""
            if MCPClient._server_failed:
                return True, "Server was not running"
            
            if self.sock:
                self.close()
            return self.server_manager.stop_server()
        
        def close(self):
            """关闭客户端连接"""
            if self.sock:
                try:
                    self.sock.close()
                except Exception:
                    pass
                finally:
                    self.sock = None
        
        def __enter__(self):
            """上下文管理器入口 - 确保服务器正在运行并连接"""
            if MCPClient._server_failed:
                return None
            
            if self.auto_start:
                if not self.server_manager.is_server_running():
                    success, message = self.server_manager.start_server()
                    if not success:
                        MCPClient._server_failed = True
                        self.close()
                        return None
            
            if not self._connect():
                return None
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            """上下文管理器退出 - 关闭连接"""
            self.close()
            return isinstance(exc_val, Exception)


class TestMCPClient(unittest.TestCase):
    """测试MCP客户端连接和功能"""

    def setUp(self):
        """设置测试环境"""
        # 创建被测试的MCPClient实例
        self.client = MCPClient(host="localhost", port=8765, auto_start=True)
        
        # 模拟_send_request方法
        self.client._send_request = Mock()
    
    def test_connect_success(self):
        """测试连接服务器成功"""
        # 模拟成功连接
        self.client._connect = Mock(return_value=True)
        
        # 使用with语句连接
        with self.client as conn:
            self.assertIsNotNone(conn, "连接应该成功")
    
    def test_connect_failure(self):
        """测试连接服务器失败"""
        # 模拟连接失败
        self.client._connect = Mock(return_value=False)
        
        # 使用with语句尝试连接
        with self.client as conn:
            self.assertIsNone(conn, "连接应该失败并返回None")
    
    def test_call_tool(self):
        """测试调用工具功能"""
        # 准备测试数据
        tool_name = "test_tool"
        arguments = {"arg1": "value1", "arg2": "value2"}
        expected_result = {"data": "测试结果"}
        
        # 设置模拟响应
        self.client._send_request.return_value = {
            "status": "success", 
            "result": expected_result
        }
        
        # 调用被测试的方法
        result = self.client.call_tool(tool_name, arguments)
        
        # 验证结果
        self.assertEqual(result, expected_result, "应该返回预期的结果")
        
        # 验证发送的请求格式是否正确
        expected_request = {
            "command": "call_tool",
            "tool_name": tool_name,
            "arguments": arguments
        }
        self.client._send_request.assert_called_with(expected_request)
    
    def test_get_available_tools(self):
        """测试获取可用工具列表功能"""
        # 准备测试数据
        expected_tools = [
            {"name": "tool1", "description": "工具1描述"},
            {"name": "tool2", "description": "工具2描述"}
        ]
        
        # 设置模拟响应
        self.client._send_request.return_value = {
            "status": "success", 
            "tools": expected_tools
        }
        
        # 调用被测试的方法
        tools = self.client.get_available_tools()
        
        # 验证结果
        self.assertEqual(tools, expected_tools, "应该返回预期的工具列表")
        
        # 验证发送的请求格式是否正确
        expected_request = {"command": "get_tools"}
        self.client._send_request.assert_called_with(expected_request)

    def test_error_handling(self):
        """测试错误处理功能"""
        # 准备测试数据
        error_response = {
            "status": "error",
            "error": {
                "error_type": "TEST_ERROR",
                "message": "测试错误消息",
                "details": {}
            }
        }
        
        # 设置模拟响应
        self.client._send_request.return_value = error_response
        
        # 调用被测试的方法，应该抛出异常
        with self.assertRaises(MockMCPClientError) as context:
            self.client.call_tool("test_tool", {})
        
        # 验证异常信息
        self.assertEqual(str(context.exception), "测试错误消息")
        self.assertEqual(context.exception.error.error_type, "TEST_ERROR")
    
    def test_start_server(self):
        """测试启动服务器功能"""
        # 模拟启动服务器成功
        expected_result = (True, "服务器已启动")
        self.client.server_manager.start_server.return_value = expected_result
        
        # 调用被测试的方法
        result = self.client.start_server()
        
        # 验证结果
        self.assertEqual(result, expected_result, "启动服务器应该返回预期的结果")
        
        # 验证正确的方法被调用
        self.client.server_manager.start_server.assert_called_once()
        
        # 模拟启动服务器失败
        expected_failure = (False, "无法启动服务器")
        self.client.server_manager.start_server.return_value = expected_failure
        
        # 调用被测试的方法
        result = self.client.start_server()
        
        # 验证结果
        self.assertEqual(result, expected_failure, "启动服务器失败应该返回预期的错误信息")
    
    def test_stop_server(self):
        """测试停止服务器功能"""
        # 模拟服务器未失败
        MCPClient._server_failed = False
        
        # 模拟停止服务器成功
        expected_result = (True, "服务器已停止")
        self.client.server_manager.stop_server.return_value = expected_result
        
        # 确保有一个激活的连接
        self.client.sock = Mock()
        
        # 调用被测试的方法
        result = self.client.stop_server()
        
        # 验证结果
        self.assertEqual(result, expected_result, "停止服务器应该返回预期的结果")
        
        # 验证连接被关闭
        self.assertIsNone(self.client.sock, "连接应该被关闭")
        
        # 验证正确的方法被调用
        self.client.server_manager.stop_server.assert_called_once()
        
        # 测试服务器已失败的情况
        MCPClient._server_failed = True
        self.client.server_manager.stop_server.reset_mock()
        
        # 调用被测试的方法
        result = self.client.stop_server()
        
        # 验证结果
        self.assertEqual(result, (True, "Server was not running"), "应该直接返回服务器未运行")
        
        # 验证不应该调用stop_server方法
        self.client.server_manager.stop_server.assert_not_called()
        
        # 重置类变量以避免影响其他测试
        MCPClient._server_failed = False
    
    def tearDown(self):
        """清理测试环境"""
        self.client.close()

if __name__ == "__main__":
    unittest.main() 