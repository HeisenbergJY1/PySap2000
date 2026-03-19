from PySap2000 import Application
from PySap2000.structure_core import Point, Frame, Cable, Area, Link
from PySap2000.global_parameters import Units, UnitSystem
from PySap2000.section import (
    FrameSection, FrameSectionType, CableSection,
    AreaSection, AreaSectionType, ShellType,
    LinkSection, LinkSectionType,
)
from PySap2000.cable.enums import CableType


with Application() as app:
    Units.set_present_units(app.model, UnitSystem.N_MM_C)

    # 创建节点
    # app.create_object(Point(no=10, x=0, y=0, z=0))
    # app.create_object(Point(no=2, x=10, y=0, z=0))
    # app.create_object(Point(no=3, x=10, y=0, z=10))
    # app.create_object(Point(no=4, x=0, y=0, z=10))

    # 创建框架截面
    # sec = FrameSection(
    #     name="W14X30",
    #     material="Q355",
    #     property_type=FrameSectionType.I_SECTION,
    #     height=353.1,        # mm
    #     width=171.5,         # mm
    #     flange_thickness=13.8,
    #     web_thickness=8.5,
    # )
    # app.create_object(sec)

    # 创建框架单元
    # app.create_object(Frame(no=1, start_point=10, end_point=3, section="W14X30"))

    # 重命名框架
    # app.rename_object(Frame(no="F1"), "F2")

    # 更新框架截面
    # frame = Frame(no="F2", section="W14X31")
    # app.update_object(frame)

    # 创建索截面
    # app.create_object(CableSection(name="CAB1", material="Q355", area=500.0))

    # 创建索单元
    # app.create_object(Cable(no=1, start_point="10", end_point="2", section="CAB1"))

    # 创建面截面 (Shell)
    # app.create_object(AreaSection(
    #     name="SLAB200",
    #     material="Q355",
    #     prop_type=AreaSectionType.SHELL,
    #     shell_type=ShellType.SHELL_THIN,
    #     membrane_thickness=200.0,
    # ))

    # 创建面单元 (3节点)
    # app.create_object(Area(no=1, points=["10", "2", "3"], section="SLAB200"))

    # 创建连接属性 (Linear)
    # app.create_object(LinkSection(
    #     name="Linear1",
    #     section_type=LinkSectionType.LINEAR,
    #     dof=[True, False, False, False, False, False],       # 只激活 U1
    #     stiffness=[1000.0, 0, 0, 0, 0, 0],                  # U1 刚度
    # ))

    # 创建连接单元 (两节点)
    # app.create_object(Link(no=1, start_point="3", end_point="4", property_name="Linear1"))

    # 创建连接单元 (单节点接地弹簧)
    # app.create_object(Link(no=2, start_point="3", is_single_joint=True))

    # ==================== 更新截面/属性 ====================

    # 更新框架截面
    # app.update_object(Frame(no="1", section="W21X44"))

    # 更新索截面
    # app.update_object(Cable(no="3", section="CAB2"))
    # app.update_object(Cable(no="2"))

    # 更新面截面
    # app.update_object(Area(no="1", section="SLAB300"))

    # 更新连接属性
    # app.update_object(Link(no="1", property_name="Linear2"))




    # # ==================== 合并选中的面单元 ====================
    # from PySap2000.selection import get_selected_objects
    # from PySap2000.edit import merge_area

    # selected = get_selected_objects(app.model)
    # area_names = selected["areas"]

    # if len(area_names) >= 2:
    #     new_name = merge_area(app.model, area_names)
    #     print(f"合并成功: {area_names} -> {new_name}")
    # else:
    #     print(f"请先在 SAP2000 中选中至少 2 个面单元 (当前选中: {len(area_names)} 个)")
    


    # # ==================== 合并选中的框架 ====================
    # from PySap2000.selection import get_selected_objects
    # from PySap2000.edit import join_frame

    # selected = get_selected_objects(app.model)
    # frame_names = selected["frames"]

    # if len(frame_names) >= 2:
    #     merged = frame_names[0]
    #     for i in range(1, len(frame_names)):
    #         result = join_frame(app.model, merged, frame_names[i])
    #         if result:
    #             merged = result
    #     print(f"合并成功: {frame_names} -> {merged}")
    # else:
    #     print(f"请先在 SAP2000 中选中至少 2 个框架 (当前选中: {len(frame_names)} 个)")
   
   
   
    # ==================== 生成计算书 ====================
    # from report import ReportGenerator

    # rg = ReportGenerator(app.model)
    # path = rg.generate("计算书.docx")
    # print(f"计算书已生成: {path}")


    # ==================== 智能创建荷载 ====================
    # from PySap2000.utils import create_smart_load_cases

    # result = create_smart_load_cases(
    #     app.model,
    #     dead_extras=["SD1", "SD2"],
    #     lives=["Live1", "Live2"],
    #     winds=["W1", "W2"],
    #     snows=["SN1"],
    # )
    # # 检查结果
    # for key, val in result.items():
    #     status = "OK" if val == 0 else f"FAIL({val})"
    #     print(f"  {key}: {status}")

# ==================== 智能创建荷载组合 ====================
    # from PySap2000.utils import create_smart_combos

    # result = create_smart_combos(
    #     None,
    #     dead_case="1.0D",
    #     live_case="1.0L",
    #     gravity_case="1.0G",
    #     earthquakes=["EX", "EY", "EZ"],
    #     winds=["w0","w90","w180","w270"],
    #     temps=["TJ", "TS"],
    #     snows=["SN1"],
    #     dry_run=True,
    # )
    # for name, val in result.items():
    #     if val == 0:
    #         status = "OK"
    #     elif val == -2:
    #         status = "SKIP"
    #     else:
    #         status = f"FAIL({val})"
    #     print(f"  {name}: {status}")


    





    














