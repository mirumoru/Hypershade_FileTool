import maya.cmds as cmds
import maya.mel as mel
import subprocess
import time
import os

# ファイルノードを取得してUIに選択リスト表示する関数
def update_file_node_list():
    file_nodes = cmds.ls(type='file')

    if not file_nodes:
        cmds.warning("Fileノードが見つかりませんでした")

        cmds.inViewMessage(amg='<hl>Fileノードが見つかりませんでした</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)
        return

    # optionMenuの内容をクリアして更新
    cmds.optionMenu('fileNodeMenu', edit=True, deleteAllItems=True)
    for node in file_nodes:
        cmds.menuItem(label=node, parent='fileNodeMenu')

# 選択されたファイルノードのテクスチャをリロードする関数
def reload_selected_file(*args):
    selected_node = cmds.optionMenu('fileNodeMenu', query=True, value=True)

    if not selected_node:
        cmds.warning("Fileノードが見つかりませんでした")

        # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg='<hl>Fileノードが見つかりませんでした</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)

        return

    # Fileノードのテクスチャファイルパスを取得
    file_path = cmds.getAttr(f"{selected_node}.fileTextureName")

    if file_path and os.path.exists(file_path):
        # テクスチャの再読み込み
        cmds.setAttr(f"{selected_node}.fileTextureName", file_path, type="string")
        print(f"Reloaded: {file_path}")
                # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg=f'{selected_node}ノードがReloadされました',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)

        return
    else:
        cmds.warning("選択されたノードにファイルが設定されていません")

        # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg='<hl>選択されたノードにファイルが設定されていません</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)


def reload_all_file_nodes(*args):
    # シーン内のすべてのファイルノードを取得
    file_nodes = cmds.ls(type='file')

    if not file_nodes:
        cmds.warning("Fileノードが見つかりません")

        # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg='<hl>Fileノードが見つかりませんでした</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)
        return

    for file_node in file_nodes:
        file_path = cmds.getAttr(f"{file_node}.fileTextureName")

        if file_path and os.path.exists(file_path):
            # テクスチャの再読み込み
            cmds.setAttr(f"{file_node}.fileTextureName", file_path, type="string")
            print(f"Reloaded: {file_path}")

            # inViewMessageを使ってメッセージを表示
            cmds.inViewMessage(amg='全てのfileノードがReloadされました',
                    pos='topCenter',
                    fade=True,
                    fadeStayTime=2000,
                    alpha=.9)
        else:
            cmds.warning(f"選択されたノードにファイルが設定されていません")

            # inViewMessageを使ってメッセージを表示
            cmds.inViewMessage(amg=f'<hl>選択されたノードにファイルが設定されていません</hl>',
                    pos='topCenter',
                    fade=True,
                    fadeStayTime=2000,
                    alpha=.9)

# 選択されたファイルノードのテクスチャ画像をプレビュー表示する関数
def preview_texture(*args):
    selected_node = cmds.optionMenu('fileNodeMenu', query=True, value=True)

    if not selected_node:
        cmds.warning("Fileノードが見つかりませんでした")

        # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg='<hl>Fileノードが見つかりませんでした</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)
        return

    # Fileノードのテクスチャファイルパスを取得
    file_path = cmds.getAttr(f"{selected_node}.fileTextureName")

    if file_path and os.path.exists(file_path):
        if cmds.window('imagePreviewWindow', exists=True):
            cmds.deleteUI('imagePreviewWindow')

        window = cmds.window('imagePreviewWindow', title="Texture Preview", widthHeight=(512, 512))
        cmds.scrollLayout()
        cmds.columnLayout(adjustableColumn=True)

        initial_width = cmds.intField('widthField', query=True, value=True)
        initial_height = cmds.intField('heightField', query=True, value=True)
        cmds.image(image=file_path, width=initial_width, height=initial_height)
        cmds.showWindow(window)
    else:
        cmds.warning("選択されたノードにファイルが設定されていません")

        # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg='<hl>選択されたノードにファイルが設定されていません</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)

# 選択されたファイルノードのフォルダを開く関数
def open_folder(*args):
    selected_node = cmds.optionMenu('fileNodeMenu', query=True, value=True)

    if not selected_node:
        cmds.warning("Fileノードが見つかりませんでした")

        # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg='<hl>Fileノードが見つかりませんでした</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)
        return

    file_path = cmds.getAttr(f"{selected_node}.fileTextureName")

    if not file_path:
        cmds.warning("選択されたノードにファイルが設定されていません")

        # inViewMessageを使ってメッセージを表示
        cmds.inViewMessage(amg='<hl>選択されたノードにファイルが設定されていません</hl>',
                pos='topCenter',
                fade=True,
                fadeStayTime=2000,
                alpha=.9)
        return

    folder_path = os.path.dirname(file_path).replace('/', '\\')
    subprocess.run(['explorer', folder_path])


# おまけエリア
# Surface Shaderを作成し、Fileノードにテクスチャを設定する関数
def create_surface_shader_with_file(file_path=None):
    # ユーザーにSurfaceShaderの名前を入力させる
    shader_name = cmds.promptDialog(title="シェーダ名設定",
                                    message="設定したいSurface Shader名を入力:",
                                    button=["OK", "Cancel"],
                                    defaultButton="OK",
                                    cancelButton="Cancel",
                                    dismissString="Cancel")
    if shader_name == "OK":
        shader_name = cmds.promptDialog(query=True, text=True)
    else:
        shader_name = "mySurfaceShader"

    # ユーザーにFileノードの名前を入力させる
    file_node_name = cmds.promptDialog(title="fileノード名設定",
                                    message="設定したいfileノード名を入力:",
                                    button=["OK", "Cancel"],
                                    defaultButton="OK",
                                    cancelButton="Cancel",
                                    dismissString="Cancel")
    if file_node_name == "OK":
        file_node_name = cmds.promptDialog(query=True, text=True)
    else:
        file_node_name = "myFileTexture"

    # Surface Shaderを作成
    shader = cmds.shadingNode('surfaceShader', asShader=True, name=shader_name)

    # Fileノードを作成
    file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=file_node_name)

    # FileノードをsurfaceShaderに接続
    cmds.connectAttr(file_node + '.outColor', shader + '.outColor')

    # file_pathが指定されている場合は、ファイルノードにファイルを設定
    if file_path:
        cmds.setAttr(file_node + '.fileTextureName', file_path, type="string")

    # 新しいシェーダーを返す
    return shader

# テクスチャファイルを選択してシェーダーを作成する関数
def file_browse_callback(*args):
    file_path = cmds.fileDialog2(fileFilter="Image Files (*.jpg *.png *.tga *.tiff *.exr)", dialogStyle=2, fm=1)
    if file_path:
        file_path = file_path[0]
        create_surface_shader_with_file(file_path)
        print("Shader created with file:", file_path)
        update_file_node_list()

# MELコマンドを使用して未使用のノードを削除
def delete_unused_nodes(*args):
    mel.eval('MLdeleteUnused;')

    # ダイアログを表示
    result = cmds.confirmDialog(
        title="Restart GUI",
        message="未使用のノードを削除したためGUIをリロードします。",
        button=["OK"],
        defaultButton="OK"
    )

    if result == "OK":
        reload_gui()

def reload_gui():
    # 既存のウィンドウが存在する場合、削除してから新しく作成
    if cmds.window("hypershadeToolWindow", exists=True):
        cmds.deleteUI("hypershadeToolWindow", window=True)

#ウィンドウがおかしい場合は#を外す
    # ウィンドウの設定(位置やサイズなど)のリセット
    #if cmds.windowPref("hypershadeToolWindow", exists=True):
    #    cmds.windowPref("hypershadeToolWindow", remove=True)

    # 関数を実行する
    cmds.evalDeferred(delayed_create_ui, lowestPriority=True)


def delayed_create_ui():
    # 0.1秒待ってからUIを作成
    time.sleep(0.1)
    create_hypershade_ui()

# ToonAutoToolを呼び出す
def call_toon_auto_tool(*args):

    try:
        # 相対インポートでToonAutoToolをインポート
        from . import ToonAutoTool

        # モジュールをロード
        ToonAutoTool.toon_ui()
    except ImportError:
        cmds.confirmDialog(title='インポートエラー', message='ToonAutoTool.pyがインポートできませんでした\n'
                                'この機能を使うには"ToonAutoTool.py"が必要です', button=['OK'])

# Hypershade_materialToolを呼び出す
def call_Hypershade_material_tool(*args):

    try:
        # 相対インポートでToonAutoToolをインポート
        from . import Hypershade_materialTool

        # モジュールをリロード
        Hypershade_materialTool.create_shader_selector_ui()
    except ImportError:
        cmds.confirmDialog(title='インポートエラー', message='Hypershade_materialTool.pyがインポートできませんでした\n'
                                'この機能を使うには"Hypershade_materialTool.py"が必要です', button=['OK'])

# ライセンス表示(Hypershade_materialToolと共通)
def show_license(*args):
    # ダイアログウィンドウが既に存在する場合は削除
    if cmds.window('license', exists=True):
        cmds.deleteUI('license')

    # ダイアログウィンドウを作成
    cmds.window('license', title="MIT License", widthHeight=(480, 370))
    cmds.columnLayout(adjustableColumn=True)

    # MIT Licenseの内容を表示
    license_text = (
        "MIT License\n\n"
        "Copyright (c) 2024 mirumoru\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
    )

    cmds.text(label=license_text, align='left', wordWrap=True, height=330)

    # OKボタンを作成し、ダイアログを閉じる
    cmds.separator(height=10, style='none') #隙間
    cmds.button(label="OK", command=lambda x: cmds.deleteUI('license'))

    cmds.showWindow('license')



### ここからUI設定
# メインのUIを作成する関数
def create_hypershade_ui():
    if cmds.window('hypershadeToolWindow', exists=True):
        cmds.deleteUI('hypershadeToolWindow')

    window = cmds.window('hypershadeToolWindow', title="Hypershade File Tool", widthHeight=(280, 400))
    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=10, style='none')

    cmds.text(label="Fileノードを選択")
    cmds.optionMenu('fileNodeMenu')

    cmds.separator(height=5, style='none')

    # 選択したテクスチャを再読み込み
    cmds.button(label="選択したテクスチャを再読み込み", command=reload_selected_file)
    cmds.separator(height=2, style='none')

    cmds.button(label="全てのテクスチャを再読み込み", command=reload_all_file_nodes)
    cmds.separator(height=2, style='none')

    # テクスチャのプレビュー
    cmds.button(label="テクスチャのプレビュー", command=preview_texture)
    cmds.separator(height=2, style='none')

    # 読み込み先フォルダを開く
    cmds.button(label="読み込み先フォルダを開く", command=open_folder)
    cmds.separator(height=2, style='none')

    # fileノードリストの更新
    cmds.button(label="fileノードリストの更新", command=lambda x: update_file_node_list())

    cmds.separator(height=5, style='none')#隙間を明ける

    ## 折りたたみエリア
    # プレビュー画像サイズ設定
    cmds.frameLayout(label="プレビュー画像の幅と高さを指定", collapsable=True, collapse=True, width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 30), (2, 50), (3, 30), (4, 50)])
    cmds.text(label="幅:")
    cmds.intField('widthField', value=512) #デフォルト512
    cmds.text(label="高さ:")
    cmds.intField('heightField', value=512) #デフォルト512
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(height=10, style='in') #仕切り

    # おまけ
    cmds.frameLayout(label="おまけ", collapsable=True, collapse=True, width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=5, style='none') #隙間

    # サーフェスシェーダー作成ボタン
    cmds.button(label="テクスチャを選択してサーフェスシェーダーを作成", command=file_browse_callback)
    cmds.separator(height=3, style='none') #隙間

    # 未使用のノードを削除する
    cmds.button(label="未使用のノードを削除する", command=delete_unused_nodes)

    cmds.separator(height=3, style='none') #隙間
    # Toon auto-create toolを表示
    cmds.button(label="Toon auto-create toolを表示", command=call_toon_auto_tool)
    cmds.separator(height=3, style='none') #隙間

    # Hypershade Material Selection Toolを表示
    cmds.button(label="Hypershade Material Toolを表示", command=call_Hypershade_material_tool)
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(height=10, style='in')#仕切り

    # About
    cmds.frameLayout(label="About", collapsable=True, collapse=True, width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="スクリプト名:Hypershade File Tool",align='left')
    cmds.text(label="作成者:mirumoru, GPT-4o",align='left')
    cmds.text(label="作成日:2024年9月5日",align='left')
    cmds.text(label="更新日:2024年12月30日",align='left')
    cmds.text(label="バージョン:v1.2",align='left')
    cmds.text(label="ライセンス:MIT License",align='left')
    cmds.separator(height=5, style='none')
    # クリック時にshow_license関数を呼び出す
    cmds.button(label="License", command=show_license)
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.showWindow(window)

    #選択リストを更新
    update_file_node_list()

# UIを作成
#create_hypershade_ui()