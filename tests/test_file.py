# -*- coding: utf-8 -*-
"""文件操作相关测试"""

import pytest
from PySap2000.file import save, Units

pytestmark = pytest.mark.file


class TestFileOperations:
    """文件操作测试"""

    def test_save(self, model):
        # 保存到当前路径
        ret = save(model)
        assert ret == 0

    def test_units_enum(self):
        assert Units.N_MM_C == 9
        assert Units.KN_M_C == 6
        assert Units.KN_MM_C == 5
