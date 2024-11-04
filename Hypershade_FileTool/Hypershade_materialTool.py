import maya.cmds as cmds
import os
import configparser

# 設定ファイルのパス
config_file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'maya', '2023', 'scripts', 'Hypershade_FileTool', 'user_data_list.ini')

# 大文字小文字を区別するための設定
class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr  # 大文字小文字をそのままにする

# ConfigParserのセットアップ
config = CaseSensitiveConfigParser()

# iniファイルを読み込む
def load_config():
    if os.path.exists(config_file_path):
        config.read(config_file_path)
    else:
        config['SHADERS'] = {}

# iniファイルに保存する
def save_config():
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

# 一時保存する選択フェイスリスト
saved_faces = []

# 選択したメッシュ or フェイスを一時保存
def save_selected_faces(*args):  # 引数に*argsを追加
    global saved_faces
    saved_faces = cmds.ls(selection=True, flatten=True)  # 選択されたフェイスを保存
    if not saved_faces:
        cmds.warning("メッシュまたはフェイスを選択してください")
        cmds.confirmDialog(
                            title="エラー",
                            message=f"メッシュまたはフェイスを選択してください",
                            button=["OK"],
                            defaultButton="OK"
                            )
    else:
        print(f"メッシュまたはフェイス:{saved_faces}を一時保存しました。。")


# 選択されたメッシュまたはフェイスにマテリアルを適用
def assign_shader_to_faces(shader_name):
    global saved_faces
    if not saved_faces:
        cmds.warning("保存されたメッシュまたはフェイスがありません。選択して保存してください。")
        cmds.confirmDialog(
                            title="エラー",
                            message=f"保存されたメッシュまたはフェイスがありません。選択して保存してください。",
                            button=["OK"],
                            defaultButton="OK"
                            )
        return

    # マテリアルのシェーディンググループを取得
    shading_group = cmds.listConnections(shader_name, type='shadingEngine')

    if not shading_group:
        cmds.warning(f"{shader_name} に接続されたシェーディンググループがありません。")
        return

    # 最初のシェーディンググループを使用
    shading_group = shading_group[0]

    try:
        # メッシュまたはフェイスをセットに追加
        cmds.sets(saved_faces, edit=True, forceElement=shading_group)
        print(f"マテリアル:{shader_name}を{saved_faces}に適応しました。")
    except Exception as e:
        cmds.warning(f"メッシュまたはフェイスの適用に失敗しました: {e}")
        cmds.confirmDialog(
                            title="エラー",
                            message=f"{shader_name}を選択したメッシュまたはフェイスへの適用に失敗しました。",
                            button=["OK"],
                            defaultButton="OK"
                            )


# マテリアル選択機能
def select_shader(shader_name):
    cmds.HypershadeWindow()
    shading_groups = cmds.listConnections(shader_name, type='shadingEngine')

    if shading_groups:
        objects = cmds.sets(shading_groups[0], q=True)
        if objects:
            cmds.select(objects)
            cmds.hyperShade(assign=shader_name)
        else:
            cmds.warning(f"{shader_name}にオブジェクトが割り当てられていないため、マテリアル自体を選択しています")

        cmds.hyperShade(selection=shader_name)
        cmds.select(clear=True)
        cmds.select(shader_name, add=True)
        cmds.hyperShade(selection=shader_name)
    else:
        cmds.warning(f"{shader_name}に接続されたシェーディング グループがありません")

# マテリアルリストを取得（新しい順に並べる）
def get_all_shaders():
    all_shaders = cmds.ls(materials=True)
    return all_shaders[::-1]

# 選択されたマテリアルのリスト
selected_shaders = []

# マテリアルリストに追加
def add_selected_shader(shader_name):
    if shader_name not in selected_shaders:
        selected_shaders.append(shader_name)
        cmds.textScrollList("shaderList", edit=True, append=shader_name)
        # INIファイルにマテリアルを保存
        config['SHADERS'][shader_name] = '1'
        save_config()
    else:
        cmds.warning(f"{shader_name} がすでにリストに含まれています。")

# マテリアルリストから削除
def remove_selected_shader():
    selected = cmds.textScrollList("shaderList", q=True, selectItem=True)
    if selected:
        for shader in selected:
            if shader in selected_shaders:
                selected_shaders.remove(shader)
                cmds.textScrollList("shaderList", edit=True, removeItem=shader)
                # INIファイルからマテリアルを削除
                config['SHADERS'].pop(shader, None)
                save_config()
    else:
        cmds.warning("削除するマテリアルを選択してください")

# マテリアルリストの読み込み
def load_selected_shaders():
    if 'SHADERS' in config:
        for shader in config['SHADERS']:
            if shader not in selected_shaders:
                selected_shaders.append(shader)
                cmds.textScrollList("shaderList", edit=True, append=shader)


# マテリアルの作成と適用
def get_material_name():
    """ユーザーにマテリアルの名前を入力させるダイアログを表示"""
    result = cmds.promptDialog(
        title='マテリアルの名前を入力してください',
        message='マテリアルの名前を入力してください(英字):',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )

    if result == 'OK':
        return cmds.promptDialog(query=True, text=True)
    return None


def apply_material():
    material_type = cmds.optionMenu('materialMenu', query=True, value=True)

    # 現在選択されているフェースもしくはオブジェクトを取得
    selected_components = cmds.ls(selection=True, flatten=True)

    if not selected_components:
        cmds.warning("オブジェクトを選択してください。")
        cmds.confirmDialog(
                            title="エラー",
                            message=f"オブジェクトを選択してください",
                            button=["OK"],
                            defaultButton="OK"
                            )
        return

    shader_name = get_material_name()
    if not shader_name:
        cmds.warning("マテリアルの作成がキャンセルされました。")
        return

# 色選択ダイアログの結果を取得
    result = cmds.colorEditor()

    # 結果を文字列から分解して、RGB と boolean に変換
    r, g, b, status = map(float, result.split())
    status = bool(int(status))  # boolean に変換 true/ false

    if not status:
        print("色の選択がキャンセルされました。")
        return

    # 選択されたRGBに変換
    rgb = [r, g, b]

    print(f"色は: R={r}, G={g}, B={b} です")

    # 新しいマテリアルを作成
    try:
        material = cmds.shadingNode(material_type, asShader=True, name=shader_name)
    except RuntimeError as e:
        cmds.error(f"マテリアルの作成に失敗しました: {e}")
        return

    # マテリアルの色を設定(surfaceShaderの判断もここ)
    color_attr = 'outColor' if material_type == 'surfaceShader' else 'color'
    cmds.setAttr(f"{material}.{color_attr}", *rgb, type='double3')

    # シェーディンググループを作成してマテリアルを接続
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{material}SG")
    cmds.connectAttr(f"{material}.outColor", f"{shading_group}.surfaceShader")

    # 選択されたフェースまたはオブジェクトの全フェースに適用
    for comp in selected_components:
        if '.f[' not in comp:  # オブジェクト全体が選択された場合、フェースを取得
            faces = cmds.ls(f"{comp}.f[*]", flatten=True)
        else:  # 既にフェースが選択されている場合
            faces = [comp]

        # フェースにシェーディンググループを適用
        for face in faces:
            cmds.sets(face, edit=True, forceElement=shading_group)

    # "add_selected_shader"の実行を確認
    if 'add_selected_shader' in globals():
        add_selected_shader(shader_name)
    else:
        print(f"Shader '{shader_name}' を管理する機能が見つかりません。")

    print(f"{material_type} マテリアル '{material}' に色 {rgb} を {selected_components} にフェースに適用しました ")



    # リストを全てクリアする
def clear_folder_list():
    """リストを全てクリアして、保存する"""
    selected_shaders.clear()  # リストをクリア
    print("フォルダリストがクリアされました")
    refresh_folder_list()  # UI上のリストを更新
    # INIファイルからマテリアルを削除
    config["SHADERS"] = {}
    save_config()  # クリアされた状態をiniファイルに保存


def refresh_folder_list():
    # フォルダリストをリフレッシュして表示
    cmds.textScrollList('shaderList', edit=True, removeAll=True)  # リストをクリア
    for folder in selected_shaders:
        cmds.textScrollList('shaderList', edit=True, append=folder)  # フォルダを追加

# ライセンス表示
def show_license_fr(*args):

    try:
        # 相対インポートでインポート
        from . import Hypershade_FileTool

        # モジュールをロード
        Hypershade_FileTool.show_license()
    except ImportError:
        cmds.confirmDialog(title='インポートエラー', message='Hypershade_FileTool.pyがインポートできませんでした\n'
                                '作成者にお問い合わせください。', button=['OK'])


# GUI作成
def create_shader_selector_ui():
    global selected_shaders

    if cmds.window("shaderSelectorWindow", exists=True):
        cmds.deleteUI("shaderSelectorWindow", window=True)

    load_config()  # iniファイルを読み込む
    selected_shaders = []

    window = cmds.window("shaderSelectorWindow", title="Hypershade Material Tool", widthHeight=(320, 390))
    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=10, style='none')

    all_shaders = get_all_shaders()

    # ポップアップメニュー
    cmds.optionMenu("shaderMenu", label="マテリアルリスト:")
    for shader in all_shaders:
        cmds.menuItem(label=shader)
    cmds.separator(height=5, style='none')

    # リスト
    def on_add_button_pressed(*args):
        selected_shader = cmds.optionMenu("shaderMenu", q=True, value=True)
        add_selected_shader(selected_shader)

    # リスト追加ボタン
    cmds.button(label="マテリアルをリスト追加", command=on_add_button_pressed)

    cmds.separator(height=5, style='none')# 隙間

    # 削除ボタン
    cmds.button(label="リストで選択したマテリアルを削除", command=lambda *args: remove_selected_shader())

    cmds.separator(height=5, style='none')# 隙間

    # リストを全てクリアするボタン
    cmds.button(label="リストを全てクリア", command=lambda x: clear_folder_list())

    cmds.separator(height=5, style='none')# 隙間

    # 追加されたマテリアルのリスト表示
    cmds.textScrollList("shaderList", numberOfRows=10, height=150, allowMultiSelection=False)

    cmds.separator(height=5, style='none')# 隙間

    # 選択ボタンの処理|ここから
    def on_select_button_pressed(*args):
        selected = cmds.textScrollList("shaderList", q=True, selectItem=True)
        if selected:
            for shader in selected:
                select_shader(shader)
        else:
            cmds.warning("リストからマテリアルを選択してください")
            cmds.confirmDialog(
                                title="エラー",
                                message=f"リストからマテリアルを選択してください",
                                button=["OK"],
                                defaultButton="OK"
                                )

    # 選択ボタン|ここまで
    cmds.button(label="マテリアルをハイパーシェードで選択", command=on_select_button_pressed)

    cmds.separator(height=10, style='in')#仕切り

    # メッシュまたはフェイスを保存ボタン
    cmds.button(label="選択しているメッシュまたはフェイスを保存", command=save_selected_faces)

    cmds.separator(height=5, style='none')# 隙間

    # メッシュまたはフェイスに適用ボタンの処理
    def on_apply_button_pressed(*args):
        selected = cmds.textScrollList("shaderList", q=True, selectItem=True)
        if selected:
            assign_shader_to_faces(selected[0])
        else:
            cmds.warning("リストからマテリアルを選択してください")
            cmds.confirmDialog(
                                title="エラー",
                                message=f"リストからマテリアルを選択してください",
                                button=["OK"],
                                defaultButton="OK"
                                )

    cmds.button(label="メッシュまたはフェイスにマテリアルを適用", command=on_apply_button_pressed)


    cmds.separator(height=10, style='in')#仕切り


    # マテリアルタイプ選択用のオプションメニュー
    cmds.optionMenu("materialMenu", label="シェーダーの選択:")
    cmds.menuItem(label='surfaceShader')
    cmds.menuItem(label='lambert')
    cmds.menuItem(label='blinn')
    cmds.menuItem(label='phong')

    cmds.separator(height=5, style='none')# 隙間

    # マテリアルの追加ボタン
    cmds.button(label='マテリアルの作成と適用', command=lambda _: apply_material())

    cmds.separator(height=10, style='in')#仕切り

    # About
    cmds.frameLayout(label="About", collapsable=True, collapse=True, width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="スクリプト名:Hypershade Material Tool",align='left')
    cmds.text(label="作成者:mirumoru, GPT-4o",align='left')
    cmds.text(label="作成日:2024年10月4日",align='left')
    cmds.text(label="更新日:2024年11月04日",align='left')
    cmds.text(label="バージョン:v0.3.1",align='left')
    cmds.text(label="ライセンス:MIT License",align='left')
    cmds.separator(height=5, style='none')
    # ボタンを作成し、クリック時にshow_license関数を呼び出す
    cmds.button(label="License", command=show_license_fr)
    cmds.setParent('..')
    cmds.setParent('..')


    load_selected_shaders()  # iniファイルからマテリアルリストを読み込む

    cmds.showWindow(window)

# GUIを表示
#create_shader_selector_ui()
