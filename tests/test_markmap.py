import os
import shutil
import unittest
import re
import unittest.mock as mock
import common.markmap  as markmap

class TestSaveMarkdownToFile(unittest.TestCase):
    """测试 markdown 文件保存功能"""
    
    def setUp(self):
        """测试前设置，确保测试目录不存在"""
        self.test_dir = "resource/md_cache"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    # def tearDown(self):
    #     """测试后清理，删除创建的测试目录"""
    #     if os.path.exists(self.test_dir):
    #         shutil.rmtree(self.test_dir)
    
    def test_save_markdown_creates_directory(self):
        """测试当目录不存在时是否会创建目录"""
        self.assertFalse(os.path.exists(self.test_dir))
        markmap.save_markdown_to_file("测试内容")
        self.assertTrue(os.path.exists(self.test_dir))
    
    def test_save_markdown_content(self):
        """测试保存的内容是否正确"""
        test_content = "# 测试标题\n\n这是测试内容"
        file_path = markmap.save_markdown_to_file(test_content)
        
        # 检查文件是否存在
        self.assertTrue(os.path.exists(file_path))
        
        # 检查文件内容是否正确
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, test_content)
    
    def test_file_naming(self):
        """测试文件命名是否符合要求"""
        file_path = markmap.save_markdown_to_file("测试内容")
        filename = os.path.basename(file_path)
        
        # 检查文件名格式
        pattern = r"模型总结_\d+\.md"
        self.assertTrue(re.match(pattern, filename))
    
    def test_custom_prefix(self):
        """测试自定义前缀"""
        custom_prefix = "自定义前缀"
        file_path = markmap.save_markdown_to_file("测试内容", prefix=custom_prefix)
        filename = os.path.basename(file_path)
        
        # 检查文件名前缀
        self.assertTrue(filename.startswith(f"{custom_prefix}_"))
        
    def test_return_path(self):
        """测试返回的路径是否有效"""
        file_path = markmap.save_markdown_to_file("测试内容")
        
        # 检查返回的路径是否存在
        self.assertTrue(os.path.exists(file_path))
        
        # 检查返回的路径是否为指定格式
        self.assertTrue(file_path.startswith(self.test_dir))
        self.assertTrue(file_path.endswith(".md"))


    def test_generate_mind_map(self):
        markdown_text = """
       # **中国农村宅基地政策分析**
- 现行政策无2025年禁止到农村购买宅基地明确规定
- 此说法可能源于对政策趋势猜测或误读
# **1. 中国农村宅基地基本政策**
- 所有权归集体，农民仅有使用权
- 禁止城市居民购买
- 农民间流转遵循“一户一宅”且限于本集体经济组织成员
# **2. “2025年禁止购买”猜测来源**
- **乡村振兴与土地制度改革**
    - 宅基地“三权分置”，允许符合条件主体租赁、合作使用
    - 防止非农化，禁止用于房地产开发
- **耕地保护与“非粮化”“非农化”整治**
    - 严守18亿亩耕地红线
    - 限制非农资本变相占用耕地
- **户籍制度改革与城乡融合**
    - 探索农民进城落户后宅基地退出机制
    - 规范非集体经济组织成员宅基地流转
- **试点政策误传**
    - 部分地区试点政策对流转设条件或时间表
    - 误传为全国性政策并关联2025年
# **3. 2025年可能政策动向**
- 规范使用权流转，扩大范围但需集体审批
- 强化用途管制，禁止用于商品房开发
- 完善退出机制，鼓励闲置宅基地优化利用
# **4. 需澄清误区**
- **“购买”与“使用权流转”区别**
    - 购买指所有权转移，宅基地不可出售
    - 使用权流转指租赁、合作等并受限
- **政策延续性**
    - 禁止城市居民购买是长期规定
    - “2025年禁止”可能是强调或误读
# **5. 官方建议**
- 查阅自然资源部、农业农村部最新文件
- 关注地方试点政策
- 咨询村委会或乡镇政府土地管理部门
# **总结**
- 无明确2025年禁止购买政策
- 未来改革可能收紧非农资本参与交易
- 强调宅基地集体所有及流转规定，关注官方动态 
        """

       # 方法1：先保存文件，再生成思维导图
        print("示例1：分步生成思维导图")
        md_path = markmap.save_markdown_to_file(markdown_text, prefix="示例思维导图")
        print(f"Markdown文件已保存至: {md_path}")
        
        html_path, status, output = markmap.generate_markmap(md_path)
        if html_path:
            print(f"思维导图已生成: {html_path}")
        else:
            print(f"生成思维导图失败: {output}")
            
if __name__ == "__main__":
    unittest.main() 