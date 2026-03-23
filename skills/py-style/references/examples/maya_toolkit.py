#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
Maya工具包示例模块
展示Maya相关的代码风格和最佳实践
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 第三方导入
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import maya.cmds as cmds
import maya.OpenMaya as om

# 标准库导入
import os
import sys
import math
import json
import random
import string
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 版本兼容性处理
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
_PY_3_ = sys.version_info.major > 2
if _PY_3_:
    from importlib import reload
    from subprocess import DEVNULL
else:
    DEVNULL = open(os.devnull, 'wb')


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 自定义异常
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
class RigError(Exception):
    """绑定工具基础异常"""
    pass


class NodeNotFoundError(RigError):
    """节点未找到异常"""
    pass


class ValidationError(RigError):
    """验证失败异常"""
    pass


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 装饰器
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def undoable(func):
    """
    添加Maya撤销记录的装饰器
    
    Args:
        func: 要包装的函数
        
    Returns:
        包装后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("An error occurred: ", e)
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)
    return wrapper


def success(show_error: bool = False, show_success: bool = False):
    """
    成功/失败处理装饰器
    
    Args:
        show_error: 是否显示错误信息
        show_success: 是否显示成功信息
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                exc_type, exc_value, exc_traceback_obj = sys.exc_info()
                msg = str(e)
                if show_error:
                    print(u"执行失败！\n%s" % msg)
                return False, msg
            else:
                if show_success and result:
                    print(u"执行成功! \n{}".format(result))
                return True, result
        
        wrapper.__doc__ = func.__doc__
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 工具函数
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def get_all_parents(obj: str) -> list:
    """
    获取物体的所有父节点，从直接父级到最顶层
    
    Args:
        obj: Maya对象名称
        
    Returns:
        list: 父节点列表
        
    Raises:
        NodeNotFoundError: 如果对象不存在
    """
    if not cmds.objExists(obj):
        raise NodeNotFoundError(u"未找到对象：%s" % obj)
    
    parents = []
    current_parent = cmds.listRelatives(obj, parent=True)
    
    while current_parent:
        parents.append(current_parent[0])
        current_parent = cmds.listRelatives(parents[-1], parent=True)
    
    return parents


def get_jnt_line(start_jnt: str) -> list:
    """
    获取关节链
    
    Args:
        start_jnt: 起始关节名称
        
    Returns:
        list: 关节列表
        
    Raises:
        NodeNotFoundError: 如果关节不存在
    """
    def _get_jnt_line(st_jnt: str, jnt_line: list) -> None:
        """
        递归获取关节链
        
        Args:
            st_jnt: 当前关节
            jnt_line: 关节列表
        """
        jnt_line.append(st_jnt)
        jnt_next = cmds.listRelatives(st_jnt, type="joint", children=True)
        if jnt_next:
            _get_jnt_line(jnt_next[0], jnt_line)
    
    if not cmds.objExists(start_jnt):
        raise NodeNotFoundError(u"未找到关节：%s" % start_jnt)
    
    jnt_line = []
    _get_jnt_line(start_jnt, jnt_line)
    return jnt_line


def attr_num(
    obj: str,
    attr: str,
    attr_type: str,
    min_val: float = None,
    max_val: float = None,
    dv: float = None,
    keyable: bool = True
) -> str:
    """
    添加数值属性
    
    Args:
        obj: 对象名称
        attr: 属性名称
        attr_type: 属性类型
        min_val: 最小值
        max_val: 最大值
        dv: 默认值
        keyable: 是否可关键帧
        
    Returns:
        str: 属性完整名称
    """
    if cmds.objExists(obj + "." + attr):
        return obj + "." + attr
    
    kwargs = {"ln": attr, "at": attr_type, "k": int(keyable)}
    
    if min_val is not None:
        kwargs["min"] = min_val
    if max_val is not None:
        kwargs["max"] = max_val
    if dv is not None:
        kwargs["dv"] = dv
    
    cmds.addAttr(str(obj), **kwargs)
    return obj + "." + attr


def attr_float(
    obj: str,
    attr: str,
    min_val: float = None,
    max_val: float = None,
    dv: float = None,
    keyable: bool = True
) -> str:
    """
    添加浮点属性
    
    Args:
        obj: 对象名称
        attr: 属性名称
        min_val: 最小值
        max_val: 最大值
        dv: 默认值
        keyable: 是否可关键帧
        
    Returns:
        str: 属性完整名称
    """
    return attr_num(obj, attr, 'double', min_val, max_val, dv, keyable)


def attr_int(
    obj: str,
    attr: str,
    min_val: int = None,
    max_val: int = None,
    dv: int = None,
    keyable: bool = True
) -> str:
    """
    添加整数属性
    
    Args:
        obj: 对象名称
        attr: 属性名称
        min_val: 最小值
        max_val: 最大值
        dv: 默认值
        keyable: 是否可关键帧
        
    Returns:
        str: 属性完整名称
    """
    return attr_num(obj, attr, 'long', min_val, max_val, dv, keyable)


def attr_bool(obj: str, attr: str, dv: int = 0, keyable: bool = True) -> str:
    """
    添加布尔属性
    
    Args:
        obj: 对象名称
        attr: 属性名称
        dv: 默认值
        keyable: 是否可关键帧
        
    Returns:
        str: 属性完整名称
    """
    return attr_num(obj, attr, 'bool', dv=dv, k=int(keyable))


def conf_naming(keyword: str, suffix: str = "") -> str:
    """
    配置命名，确保名称唯一
    
    Args:
        keyword: 关键字
        suffix: 后缀
        
    Returns:
        str: 唯一名称
        
    Raises:
        KeyError: 如果无法生成唯一名称
    """
    for k in string.ascii_uppercase:
        for i in range(100):
            h_word = keyword + '_%s%d' % (k, i + 1)
            if suffix:
                h_word += "_%s" % suffix
            if not cmds.objExists(h_word):
                return h_word
    
    raise KeyError('Please enter an identifying name')


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++ #
# Maya曲线工具类
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++ #
class CurveTool(object):
    """Maya曲线操作工具类"""
    
    def __init__(self, keyword: str = "Curve"):
        """
        初始化曲线工具
        
        Args:
            keyword: 命名关键字
        """
        self.keyword = keyword
    
    @undoable
    def build_curve_by_txt(self, name: str, text: str) -> str:
        """
        根据文本创建曲线
        
        Args:
            name: 曲线名称
            text: 文本内容
            
        Returns:
            str: 曲线变换节点名称
        """
        # 解锁节点
        cmds.lockNode('initialParticleSE', lock=False, lockUnpublished=False)
        cmds.lockNode('initialShadingGroup', lock=False, lockUnpublished=False)
        cmds.lockNode('renderPartition', lock=False, lockUnpublished=False)
        
        # 导入类型工具设置
        import maya.app.type.typeToolSetup as ts
        ts.createTypeTool(font="Lucida Console", text=text, legacy=False)
        
        # 刷新视图
        cmds.refresh()
        
        # 获取当前选择的变换节点
        type_transform = cmds.ls(selection=True)[0]
        
        # 执行 MEL 命令
        cmds.evalEcho("convertTypeCapsToCurves;")
        
        # 获取当前选择的曲线
        type_curve = cmds.ls(selection=True)[0]
        
        # 创建新的变换节点
        curve_trans = cmds.createNode("transform", name=name, skipSelect=True)
        
        # 获取曲线形状
        shapes = cmds.listRelatives(type_curve, type="nurbsCurve", allDescendents=True)
        
        # 将形状重新父化到新的变换节点
        for shape in shapes:
            cmds.parent(shape, curve_trans, relative=True, shape=True)
        
        # 刷新视图
        cmds.refresh()
        
        # 删除旧的曲线和变换节点
        cmds.delete(type_curve, type_transform)
        
        # 重命名形状
        shapes = cmds.listRelatives(curve_trans, shapes=True, type="nurbsCurve", allDescendents=True)
        for i, s in enumerate(shapes):
            new_name = "{name}Shape{number}".format(name=name, number=i + 1)
            cmds.rename(s, new_name)
        
        # 选择新的变换节点
        cmds.select(curve_trans, replace=True)
        
        return curve_trans
    
    def _get_points_by_curve(self, curve: str, number: int) -> list:
        """
        获取曲线上的点
        
        Args:
            curve: 曲线名称
            number: 点的数量
            
        Returns:
            list: 点坐标列表
        """
        parameter_list = [float(i) / (number - 1) for i in range(number)]
        points = []
        
        p_on_curve = cmds.createNode("pointOnCurveInfo")
        cmds.setAttr(f'{p_on_curve}.turnOnPercentage', True)
        cmds.connectAttr(f'{curve}.worldSpace[0]', f'{p_on_curve}.inputCurve', force=True)
        
        for parameter in parameter_list:
            cmds.setAttr(f'{p_on_curve}.parameter', parameter)
            pos = cmds.getAttr(f'{p_on_curve}.result.position')[0]
            points.append(pos)
        
        cmds.delete(p_on_curve)
        
        return points
    
    def build_curve_by_number(self, curves: list, num: int, curve_name: str) -> str:
        """
        根据数量创建曲线
        
        Args:
            curves: 源曲线列表
            num: 控制器数量
            curve_name: 新曲线名称
            
        Returns:
            str: 新曲线名称
        """
        parameter_list = [float(i) / (num - 1) for i in range(num)]
        p_on_curve = cmds.createNode("pointOnCurveInfo")
        cmds.setAttr(f'{p_on_curve}.turnOnPercentage', True)
        
        points = []
        for curve in curves:
            _pos = []
            cmds.connectAttr(f'{curve}.worldSpace[0]', f'{p_on_curve}.inputCurve', force=True)
            
            for parameter in parameter_list:
                cmds.setAttr(f'{p_on_curve}.parameter', parameter)
                pos = cmds.getAttr(f'{p_on_curve}.result.position')[0]
                _pos.append(pos)
            
            points.append(_pos)
        
        cmds.delete(p_on_curve)
        
        # 计算平均点
        ep = []
        for ps in zip(*points):
            length = len(ps)
            x, y, z = list(zip(*ps))
            ep.append([sum(x) / length, sum(y) / length, sum(z) / length])
        
        # 创建曲线
        curve = cmds.curve(d=3, ep=ep)
        curve = cmds.rename(curve, curve_name)
        
        return curve


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++ #
# Maya关节工具类
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++ #
class JointTool(object):
    """Maya关节操作工具类"""
    
    def __init__(self, keyword: str = "Joint"):
        """
        初始化关节工具
        
        Args:
            keyword: 命名关键字
        """
        self.keyword = keyword
    
    @undoable
    def orient_joint(
        self,
        line_jnts: list,
        pri_axis: str = "X",
        sec_axis: str = "Y",
        keep_end: bool = False
    ) -> None:
        """
        矫正关节方向
        
        Args:
            line_jnts: 关节列表
            pri_axis: 主轴
            sec_axis: 次轴
            keep_end: 是否保持末端关节方向
        """
        if keep_end:
            end_or = cmds.getAttr(f'{line_jnts[-1]}.jointOrient')
        
        # 获取基础信息
        jnt_infs = {}
        for jnt in line_jnts:
            tpos = cmds.xform(jnt, query=True, worldSpace=True, translation=True)
            trans = cmds.getAttr(f'{jnt}.translate')[0]
            children = cmds.listRelatives(jnt, children=True, type='joint')
            jnt_infs.setdefault(jnt, [trans, tpos, children[0] if children else None])
        
        st_jnt = line_jnts[0]
        ed_jnt = line_jnts[-1]
        parents = get_all_parents(ed_jnt)
        
        assert st_jnt in parents, RuntimeError("{} is not the parent of {}".format(ed_jnt, st_jnt))
        
        get_p = cmds.listRelatives(st_jnt, parent=True)
        if get_p:
            cmds.parent(st_jnt, world=True)
        
        # 断开父子关系
        for vals in jnt_infs.values():
            children = vals[2]
            if children:
                cmds.parent(children, world=True)
        
        # 重新建立父子关系
        rev = list(reversed(line_jnts))
        for i, c in enumerate(rev[:-1]):
            cmds.parent(c, rev[i + 1])
        
        # 矫正关节方向
        self._fit_mode_update_joints(line_jnts, recursive=0, pri_axis=pri_axis, sec_axis=sec_axis)
        
        if keep_end:
            cmds.setAttr(f'{line_jnts[-1]}.jointOrient', *end_or, type='double3')
        
        if get_p:
            cmds.parent(st_jnt, get_p[0])
    
    def _fit_mode_update_joints(
        self,
        line_jnts: list,
        recursive: int = 0,
        pri_axis: str = "X",
        sec_axis: str = "Y"
    ) -> None:
        """
        更新关节方向（简化版）
        
        Args:
            line_jnts: 关节列表
            recursive: 是否递归
            pri_axis: 主轴
            sec_axis: 次轴
        """
        # 这里应该调用实际的关节方向更新逻辑
        # 示例中使用Maya的orientJoint命令
        if line_jnts:
            for jnt in line_jnts:
                # 实际实现中会使用更复杂的逻辑
                pass
    
    def build_joint_by_number(
        self,
        curve: str,
        number: int,
        axis_root_jnt: str = None
    ) -> list:
        """
        根据数量创建关节
        
        Args:
            curve: 曲线名称
            number: 关节数量
            axis_root_jnt: 根关节（用于对齐）
            
        Returns:
            list: 关节列表
        """
        points = self._get_points_by_curve(curve, number)
        
        # 创建骨骼
        jnt_suffix = self.keyword + "_jnt"
        start_jnt = axis_root_jnt
        line_jnt = []
        
        for i, p in enumerate(points):
            cmds.select(clear=True)
            current_jnt = cmds.joint(name=jnt_suffix + "_%d" % (i + 1))
            cmds.xform(current_jnt, worldSpace=True, translation=p)
            
            if start_jnt:
                constraint = cmds.orientConstraint(start_jnt, current_jnt, maintainOffset=False)[0]
                cmds.delete(constraint)
                cmds.parent(current_jnt, start_jnt)
            
            start_jnt = current_jnt
            line_jnt.append(start_jnt)
        
        if axis_root_jnt:
            attr_bool(line_jnt[0], "freeOrient", 1, 1)
        
        # 矫正骨骼
        self.orient_joint(line_jnt, pri_axis="X", sec_axis="-Y")
        
        return line_jnt
    
    def _get_points_by_curve(self, curve: str, number: int) -> list:
        """
        获取曲线上的点
        
        Args:
            curve: 曲线名称
            number: 点的数量
            
        Returns:
            list: 点坐标列表
        """
        parameter_list = [float(i) / (number - 1) for i in range(number)]
        points = []
        
        p_on_curve = cmds.createNode("pointOnCurveInfo")
        cmds.setAttr(f'{p_on_curve}.turnOnPercentage', True)
        cmds.connectAttr(f'{curve}.worldSpace[0]', f'{p_on_curve}.inputCurve', force=True)
        
        for parameter in parameter_list:
            cmds.setAttr(f'{p_on_curve}.parameter', parameter)
            pos = cmds.getAttr(f'{p_on_curve}.result.position')[0]
            points.append(pos)
        
        cmds.delete(p_on_curve)
        
        return points


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 主类示例
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
class RigBuilder(object):
    """
    绑定构建器
    
    属性:
        keyword: 命名关键字
        root_jnt: 根关节
        curve: 曲线列表
        ctrl_num: 控制器数量
        jnt_num: 关节数量
    """
    
    # 类属性
    dy_top_grp = "dyn_chains_ws_grp"
    dy_out_c_grp = "dyn_chains_out_c_grp"
    dy_ik_grp = "dyn_chains_ik_grp"
    dy_ctrl_grp = "dyn_chains_ctrl_grp"
    dy_jnt_fit_grp = "dyn_chains_fit_grp"
    
    def __init__(self):
        """初始化构建器"""
        self._keyword = ""
        self._root_jnt = ""
        self._curve = []
        self._ctrl_num = 2
        self._jnt_num = 2
        self._ctrl_using_dis = False
        self._jnt_using_dis = False
        self._ctrl_dis = 0.0
        self._jnt_dis = 0.0
    
    @property
    def keyword(self) -> str:
        """命名关键字"""
        return self._keyword
    
    @keyword.setter
    def keyword(self, value: str):
        self._keyword = value
    
    @property
    def root_jnt(self) -> str:
        """根关节"""
        return self._root_jnt
    
    @root_jnt.setter
    def root_jnt(self, value: str):
        assert cmds.objExists(value), KeyError(u"没有找到根骨骼：%s" % value)
        self._root_jnt = value
    
    @property
    def curve(self) -> list:
        """曲线列表"""
        return self._curve
    
    @curve.setter
    def curve(self, value: list):
        assert isinstance(value, (set, list)), RuntimeError("curve 需要列表类型")
        self._curve = value
    
    @property
    def ctrl_num(self) -> int:
        """控制器数量"""
        return self._ctrl_num
    
    @ctrl_num.setter
    def ctrl_num(self, value: int):
        assert isinstance(value, int), KeyError("ctrl number 需要整数类型")
        self._ctrl_using_dis = False
        self._ctrl_num = value
    
    @property
    def jnt_num(self) -> int:
        """关节数量"""
        return self._jnt_num
    
    @jnt_num.setter
    def jnt_num(self, value: int):
        assert isinstance(value, int), KeyError("joint number 需要整数类型")
        self._jnt_using_dis = False
        self._jnt_num = value
    
    @undoable
    def build(self) -> dict:
        """
        构建绑定
        
        Returns:
            dict: 构建结果信息
        """
        keyword = self.keyword
        assert keyword, KeyError("没有输入命名关键字")
        
        curve = self.curve
        assert curve, KeyError("没有输入曲线")
        
        # 创建关节
        joint_tool = JointTool(keyword)
        jnts = joint_tool.build_joint_by_number(curve[0], self.jnt_num, self.root_jnt)
        
        # 创建控制器
        ctrl_num = self.ctrl_num
        curve_tool = CurveTool(keyword)
        ctrl_curve = curve_tool.build_curve_by_number(curve, ctrl_num, f"{keyword}_ctrl_crv")
        
        return {
            "joints": jnts,
            "controllers": ctrl_curve,
            "status": "success"
        }


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 验证函数
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def validate_rig(rig_data: dict) -> tuple:
    """
    验证绑定数据
    
    Args:
        rig_data: 绑定数据字典
        
    Returns:
        tuple: (是否成功, 消息)
    """
    if not rig_data:
        return False, "绑定数据为空"
    
    joints = rig_data.get("joints", [])
    if not joints:
        return False, "没有找到关节"
    
    for jnt in joints:
        if not cmds.objExists(jnt):
            return False, u"关节不存在：%s" % jnt
    
    return True, "验证成功"


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 主程序入口
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def main():
    """主函数"""
    try:
        # 创建构建器
        builder = RigBuilder()
        builder.keyword = "TestRig"
        builder.ctrl_num = 5
        builder.jnt_num = 10
        
        # 获取选中的曲线
        selection = cmds.ls(selection=True)
        if not selection:
            raise ValidationError("请先选择曲线")
        
        builder.curve = selection
        
        # 构建绑定
        result = builder.build()
        
        # 验证结果
        valid, msg = validate_rig(result)
        if valid:
            print("绑定构建成功！")
            print("关节:", result["joints"])
            print("控制器:", result["controllers"])
        else:
            raise ValidationError(msg)
    
    except Exception as e:
        print("绑定构建失败：", str(e))
        raise


if __name__ == "__main__":
    main()
