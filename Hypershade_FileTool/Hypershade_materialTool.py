import maya.cmds as cmds
import os
import configparser

# 大文字小文字を区別するための設定
class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr  # 大文字小文字をそのままにする

# ConfigParserのセットアップ
config = CaseSensitiveConfigParser()

# INIファイルのディレクトリ
base_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'maya', '2023', 'scripts', 'Hypershade_FileTool', 'userdata')
os.makedirs(base_dir, exist_ok=True)

# 現在のシーン名を取得
scene_name = cmds.file(q=True, sceneName=True, shortName=True) or "unsaved_scene"
scene_name_no_ext = os.path.splitext(scene_name)[0].replace('/', '\\')

# 設定ファイルのパス
config_file_path = os.path.join(base_dir, f'{scene_name_no_ext}.ini').replace('/', '\\')

# iniファイルを読み込む
def load_config(file_path=config_file_path):
    global config
    if os.path.exists(file_path):
        config.read(file_path)
        print(f"INIファイル {file_path} を読み込みました。")
    else:
        config['SHADERS'] = {}
        print(f"INIファイル {file_path} が見つかりませんでした。新規作成します。")

# iniファイルに保存する
def save_config():
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)
        print(f"INIファイル {config_file_path} に保存しました。")


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

# マテリアルリストの読み込み
def load_selected_shaders():
    if 'SHADERS' in config:
        for shader in config['SHADERS']:
            if shader not in selected_shaders:
                selected_shaders.append(shader)
                cmds.textScrollList("shaderList", edit=True, append=shader)


# 選択オブジェクトのマテリアル名を取得してリストに追加する関数
def add_selected_shader_from_object():

    # スクロールリストの既存項目を取得
    existing_items = cmds.textScrollList("shaderList", query=True, allItems=True) or []

    # 選択オブジェクトの取得
    selected_objects = cmds.ls(selection=True, long=True)
    if not selected_objects:
        cmds.textScrollList("shaderList", edit=True, append="No objects selected.")
        return

    # マテリアル名を取得
    new_materials = []
    for obj in selected_objects:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        for shape in shapes:
            shading_groups = cmds.listConnections(shape, type="shadingEngine") or []
            for sg in shading_groups:
                materials = cmds.listConnections(sg + ".surfaceShader") or []
                new_materials.extend(materials)

    # `existing_items` に含まれる重複するマテリアルを検出
    duplicates = [material for material in new_materials if material in existing_items]
    if duplicates:
        cmds.warning("既存リストと重複しているマテリアル名:", ", ".join(set(duplicates)))

    # 重複を削除して新しいマテリアルのみを追加
    unique_materials = sorted(set(new_materials) - set(existing_items))
    if unique_materials:
        for material in unique_materials:
            cmds.textScrollList("shaderList", edit=True, append=material)
            config['SHADERS'][material] = '1'
            save_config()
    else:
        if not existing_items:
            cmds.textScrollList("shaderList", edit=True, append="選択したオブジェクトに新しいマテリアルは割り当てられていません。")



# マテリアルリストから削除
def remove_selected_shader():
    # スクロールリストで選択された項目を取得
    selected = cmds.textScrollList("shaderList", q=True, selectItem=True)
    if selected:
        for shader in selected:
            # スクロールリストから削除
            cmds.textScrollList("shaderList", edit=True, removeItem=shader)
            # configから削除（configが存在する場合）
            if 'config' in globals() and 'SHADERS' in config:
                config['SHADERS'].pop(shader, None)
        # 設定を保存（必要な場合）
        if 'save_config' in globals():
            save_config()
    else:
        cmds.warning("削除するマテリアルを選択してください")

# INIファイルを読み込んでリストを更新する
def load_ini_file():
    file_path = cmds.fileDialog2(dialogStyle=2, fileMode=1, startingDirectory=base_dir, fileFilter="*.ini")
    if file_path:
        ini_path = file_path[0].replace('/', '\\')  # Mayaのファイルパスに合わせてスラッシュを変換
        clear_folder_list() # リストを初期化
        load_config(ini_path)  # INIファイルを読み込む
        update_shader_list()  # INIデータでリストを更新する

# リストを更新する
def update_shader_list():
    global selected_shaders
    selected_shaders.clear()
    cmds.textScrollList("shaderList", edit=True, removeAll=True)
    if 'SHADERS' in config:
        for shader in config['SHADERS'].keys():  # キーのみを取得
            selected_shaders.append(shader)
            cmds.textScrollList("shaderList", edit=True, append=shader)
            save_config()
    print("リストを更新しました:", selected_shaders)


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
        print(f"マテリアル:{shader_name}を{saved_faces}に適用しました。")
    except Exception as e:
        cmds.warning(f"メッシュまたはフェイスの適用に失敗しました: {e}")
        cmds.confirmDialog(
            title="エラー",
            message=f"{shader_name}を選択したメッシュまたはフェイスへの適用に失敗しました。",
            button=["OK"],
            defaultButton="OK"
        )


# ハイパーシェードでマテリアル選択機能
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


# マテリアルを選択してオブジェクトを選択する
def select_material_object(shader_name):
    shading_groups = cmds.listConnections(shader_name, type='shadingEngine')

    if shading_groups:
        objects = cmds.sets(shading_groups[0], q=True)
        if objects:
            cmds.select(objects)
            print(f"{shader_name}が割り当てられているオブジェクトを選択しました。")
        else:
            cmds.warning(f"{shader_name}に割り当てられているオブジェクトが見つかりません。")
    else:
        cmds.warning(f"{shader_name}に関連するシェーディンググループが見つかりません。")


# 選択項目の分離
def isolate_last_model_panel(*args):
    # 全ての modelPanel を取得
    all_model_panels = [panel for panel in cmds.getPanel(allPanels=True) if cmds.modelPanel(panel, query=True, exists=True)]

    # modelPanel が存在しない場合
    if not all_model_panels:
        print("モデルパネルが見つかりません。")
        print("isolateSelect 操作をスキップします。")
    else:
        # 最後の modelPanel を取得
        last_model_panel = all_model_panels[-1]
        print(f"最後のモデルパネル: '{last_model_panel}'")

        # アイソレート選択の現在の状態を取得
        current_state = cmds.isolateSelect(last_model_panel, query=True, state=True)

        if current_state:
            # 既に有効なら無効にする
            cmds.isolateSelect(last_model_panel, state=0)
            print(f"選択パネル '{last_model_panel}' が無効")
        else:
            # 無効なら有効にして選択物を追加
            cmds.isolateSelect(last_model_panel, state=1)
            cmds.isolateSelect(last_model_panel, addSelected=True)
            print(f"選択パネル ''{last_model_panel}' が有効")


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
# ===============================================
# ===============================================
# ===============================================
# ===============================================
# GUI作成
def create_shader_selector_ui():
    global selected_shaders

    if cmds.window("shaderSelectorWindow", exists=True):
        cmds.deleteUI("shaderSelectorWindow", window=True)

    load_config()  # iniファイルを読み込む
    selected_shaders = []

    window = cmds.window("shaderSelectorWindow", title="Hypershade Material Tool", widthHeight=(550, 870))
    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=10, style='none')

    all_shaders = get_all_shaders()

    # アイテムメニュー
    cmds.optionMenu("shaderMenu", label="マテリアルリスト:")
    for shader in all_shaders:
        cmds.menuItem(label=shader)
    cmds.separator(height=5, style='none')


    # リスト
    def add_materials_from_selection_to_list(*args):
        selected_shader = cmds.optionMenu("shaderMenu", q=True, value=True)
        add_selected_shader(selected_shader)

    # リスト追加ボタン
    cmds.button(label="マテリアル名をリストへ追加", command=add_materials_from_selection_to_list)

    cmds.separator(height=5, style='none')# 隙間

    # 選択したオブジェクトから追加ボタン
    cmds.button(label="オブジェクトからマテリアル名を追加", command=lambda x: add_selected_shader_from_object())

    cmds.separator(height=5, style='none')# 隙間

    # 削除ボタン
    cmds.button(label="リストで選択したマテリアルを削除", command=lambda x: remove_selected_shader())

    cmds.separator(height=5, style='none')# 隙間

    # リストを全てクリアするボタン
    cmds.button(label="リストを全てクリア", command=lambda x: clear_folder_list())

    cmds.separator(height=5, style='none')# 隙間

    # 追加されたマテリアルのリスト表示
    cmds.textScrollList("shaderList", numberOfRows=10, height=150, allowMultiSelection=False)

    cmds.separator(height=5, style='none')# 隙間

    # 選択ボタンの処理ハイパーシェードのみ|ここから
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
    cmds.button(label="リストで選択しているマテリアルをHypershadeで選択", command=on_select_button_pressed)

    cmds.separator(height=5, style='none')# 隙間

        # 選択ボタンの処理オブジェクト選択|ここから
    def on_select_material_object(*args):
        selected = cmds.textScrollList("shaderList", q=True, selectItem=True)
        if selected:
            for shader in selected:
                select_material_object(shader)
        else:
            cmds.warning("リストからマテリアルを選択してください")
            cmds.confirmDialog(
                                title="エラー",
                                message=f"リストからマテリアルを選択してください",
                                button=["OK"],
                                defaultButton="OK"
                                )

    # 選択したマテリアルが適用されたオブジェクトを選択|ここまで
    cmds.button(label="リストで選択しているマテリアルを選択状態にする", command=on_select_material_object)

    cmds.separator(height=5, style='none')# 隙間

    cmds.button(label="選択項目の分離", command=isolate_last_model_panel)

    cmds.separator(height=10, style='in')#仕切り

    # メッシュまたはフェイスを保存ボタン
    cmds.button(label="1.選択しているメッシュまたはフェイスを保存", command=save_selected_faces)

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

    cmds.button(label="2.メッシュまたはフェイスにリストで選択しているマテリアルを適用", command=on_apply_button_pressed)


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

    # インポート
    cmds.frameLayout(label="インポート", collapsable=True, collapse=True, width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=5, style='none')# 隙間
    cmds.button(label="リスト設定ファイル(ini)をインポート", command=lambda _: load_ini_file())
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(height=5, style='none')# 隙間

    # About
    cmds.frameLayout(label="About", collapsable=True, collapse=True, width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="スクリプト名:Hypershade Material Tool",align='left')
    cmds.text(label="作成者:mirumoru, GPT-4o",align='left')
    cmds.text(label="作成日:2024年10月4日",align='left')
    cmds.text(label="更新日:2024年12月30日",align='left')
    cmds.text(label="バージョン:v0.5",align='left')
    cmds.text(label="ライセンス:MIT License",align='left')
    cmds.separator(height=5, style='none')
    # ボタンを作成し、クリック時にshow_license関数を呼び出す
    cmds.button(label="License", command=show_license_fr)
    cmds.setParent('..')# 隙間
    cmds.setParent('..')# 隙間

    load_selected_shaders()  # iniファイルからマテリアルリストを読み込む

    cmds.showWindow(window)

# GUIを表示
#create_shader_selector_ui()