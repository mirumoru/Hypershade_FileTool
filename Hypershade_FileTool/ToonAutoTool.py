import maya.cmds as cmds

# ファイル選択用の関数
def choose_file(label):
    file_path = cmds.fileDialog2(fileMode=1, caption=label)
    if file_path:
        return file_path[0]
    return None

# toon_shaderのスクリプト
def toon_shader():
    surface_shader = cmds.shadingNode('surfaceShader', asShader=True, name='test_toon_shader')
    blend_colors1 = cmds.shadingNode('blendColors', asUtility=True, name='blendColors1')
    cmds.connectAttr(blend_colors1 + '.output', surface_shader + '.outColor', force=True)
    ramp_shader1 = cmds.shadingNode('rampShader', asShader=True, name='rampShader1')
    cmds.connectAttr(ramp_shader1 + '.outColorR', blend_colors1 + '.blender', force=True)
    blend_colors2 = cmds.shadingNode('blendColors', asUtility=True, name='blendColors2')
    cmds.connectAttr(blend_colors2 + '.output', blend_colors1 + '.color2', force=True)

    cmds.confirmDialog(title='通知', message='ハイライト用のテクスチャを選択します', button=['OK'])

    highlight_file = choose_file('Select Highlight Image')
    if highlight_file:
        file_highlight = cmds.shadingNode('file', asUtility=True, name='file_highlight')
        cmds.setAttr(file_highlight + '.fileTextureName', highlight_file, type='string')
        cmds.connectAttr(file_highlight + '.outColor', blend_colors1 + '.color1', force=True)

        cmds.confirmDialog(title='通知', message='カラー用のテクスチャを選択します', button=['OK'])

    color_file = choose_file('Select Color Image')
    if color_file:
        file_color = cmds.shadingNode('file', asUtility=True, name='file_color')
        cmds.setAttr(file_color + '.fileTextureName', color_file, type='string')
        cmds.connectAttr(file_color + '.outColor', blend_colors2 + '.color1', force=True)

    ramp_shader2 = cmds.shadingNode('rampShader', asShader=True, name='rampShader2')
    cmds.connectAttr(ramp_shader2 + '.outColorR', blend_colors2 + '.blender', force=True)

    cmds.confirmDialog(title='通知', message='シャドー(影)用のテクスチャを選択します', button=['OK'])

    shadow_file = choose_file('Select Shadow Image')
    if shadow_file:
        file_shadow = cmds.shadingNode('file', asUtility=True, name='file_shadow')
        cmds.setAttr(file_shadow + '.fileTextureName', shadow_file, type='string')
        cmds.connectAttr(file_shadow + '.outColor', blend_colors2 + '.color2', force=True)

# toon_shader_noのスクリプト
def toon_shader_no():
    surface_shader = cmds.shadingNode('surfaceShader', asShader=True, name='toon_shader')
    blend_colors1 = cmds.shadingNode('blendColors', asUtility=True, name='blendColors1')
    cmds.connectAttr(blend_colors1 + '.output', surface_shader + '.outColor', force=True)
    ramp_shader1 = cmds.shadingNode('rampShader', asShader=True, name='rampShader1')
    cmds.connectAttr(ramp_shader1 + '.outColorR', blend_colors1 + '.blender', force=True)
    blend_colors2 = cmds.shadingNode('blendColors', asUtility=True, name='blendColors2')
    cmds.connectAttr(blend_colors2 + '.output', blend_colors1 + '.color2', force=True)
    file_highlight = cmds.shadingNode('file', asUtility=True, name='file_highlight')
    cmds.connectAttr(file_highlight + '.outColor', blend_colors1 + '.color1', force=True)
    file_color = cmds.shadingNode('file', asUtility=True, name='file_color')
    cmds.connectAttr(file_color + '.outColor', blend_colors2 + '.color1', force=True)
    ramp_shader2 = cmds.shadingNode('rampShader', asShader=True, name='rampShader2')
    cmds.connectAttr(ramp_shader2 + '.outColorR', blend_colors2 + '.blender', force=True)
    file_shadow = cmds.shadingNode('file', asUtility=True, name='file_shadow')
    cmds.connectAttr(file_shadow + '.outColor', blend_colors2 + '.color2', force=True)

# ラジオボタンで選択されたスクリプトを実行する関数
def execute_selected_script():
    selected = cmds.radioButtonGrp(script_radio_grp, q=True, select=True)
    if selected == 1:
        toon_shader()
    elif selected == 2:
        toon_shader_no()

# UIの作成
if cmds.window("toon", exists=True):
    cmds.deleteUI("toon")

window = cmds.window("toon", title="Toon auto-create tool", widthHeight=(380, 50))
cmds.columnLayout(adjustableColumn=True)

# ラジオボタンの作成
script_radio_grp = cmds.radioButtonGrp(
    numberOfRadioButtons=2,
    label='ファイル選択の有無:',
    labelArray2=['あり', 'なし'],
    select=1,
    #columnWidth2=[50, 30],  # ラベルとボタンの幅を調整
    #adjustableColumn=False  # 列を自動調整しない
)

# 実行ボタンの作成
cmds.button(label="作成", command=lambda x: execute_selected_script())

cmds.showWindow(window)

#スクリプト名:Toon auto-create tool
#参考先:https://x.com/tajiman_vrc/status/1568527678554406913
#作成者:mirumoru, GPT-4o
#作成日:2024年9月5日
#更新日:2024年10月4日

#        MIT License
#        Copyright (c) 2024 mirumoru
#        Permission is hereby granted, free of charge, to any person obtaining a copy
#        of this software and associated documentation files (the \"Software\"), to deal
#        in the Software without restriction, including without limitation the rights
#        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#        copies of the Software, and to permit persons to whom the Software is
#        furnished to do so, subject to the following conditions:
#        The above copyright notice and this permission notice shall be included in all
#        copies or substantial portions of the Software.
#        THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#        SOFTWARE.
