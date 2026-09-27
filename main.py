import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        layout.add_widget(Label(text='[size=60sp]⚙️[/size]', markup=True, size_hint_y=None, height=80))
        layout.add_widget(Label(text='[b][size=32sp][color=ffffff]CONSTRUYE.PRO[/color][/size][/b]', markup=True, size_hint_y=None, height=40))
        layout.add_widget(Label(text='[b][size=14sp][color=00e5ff]INGENIERÍA EN TUS MANOS[/color][/size][/b]', markup=True, size_hint_y=None, height=25))
        layout.add_widget(Label(text='NORMA TÉCNICA RNE E.060 / CAPECO', font_size='11sp', size_hint_y=None, height=20))
        layout.add_widget(Label(text='[color=a0a0b0]Cargando motor de dosificación técnica...[/color]', markup=True, font_size='12sp'))
        self.add_widget(layout)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        panel = TabbedPanel(do_default_tab=False)
        tab1 = TabbedPanelHeader(text='🏗️ 1. Vaciado')
        layout1 = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout1.add_widget(Label(text='[b]⚙️ CONSTRUYE.PRO - Norma RNE / CAPECO[/b]', markup=True, font_size='20sp', size_hint_y=None, height=35))
        layout1.add_widget(Label(text='1. Elemento Estructural & Proporción CAPECO:', size_hint_y=None, height=22))
        self.tipo_spinner = Spinner(
            text="Losa Aligerada/Vigas/Cols (f'c 210) [1 : 2 : 2]",
            values=(
                "Losa Aligerada/Vigas/Cols (f'c 210) [1 : 2 : 2]",
                "Pavimentos/Muros/Veredas (f'c 175) [1 : 2.5 : 2.5]",
                "Pavimentos con Hormigón (f'c 175) [1 : 5]",
                "Sub-bases y Solados (f'c 140) [1 : 6]",
                "Cimentación Corrida (Ciclópeo 1:10 + 30% PG)",
                "Dosificación Personalizada (Manual)"
            ),
            size_hint_y=None, height=45
        )
        self.tipo_spinner.bind(text=self.actualizar_info_dosif)
        layout1.add_widget(self.tipo_spinner)
        self.dosif_info_label = Label(
            text='[color=ff9f0a][b]👉 DOSIFICACIÓN CAPECO [1 : 2 : 2] POR BOLSA (42.5kg = 1 p³):[/b]\n1 Bolsa Cemento + 3.1 Baldes Arena + 3.1 Baldes Piedra + 1.1 Baldes Agua[/color]',
            markup=True, size_hint_y=None, height=50, font_size='12sp'
        )
        layout1.add_widget(self.dosif_info_label)
        layout1.add_widget(Label(text='2. Dimensiones (Largo m x Ancho m x Espesor cm):', size_hint_y=None, height=22))
        grid_medidas = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=40)
        self.input_largo = TextInput(text='5.0', hint_text='Largo (m)', multiline=False, input_filter='float')
        self.input_ancho = TextInput(text='4.0', hint_text='Ancho (m)', multiline=False, input_filter='float')
        self.input_espesor = TextInput(text='12', hint_text='Espesor (cm)', multiline=False, input_filter='float')
        grid_medidas.add_widget(self.input_largo)
        grid_medidas.add_widget(self.input_ancho)
        grid_medidas.add_widget(self.input_espesor)
        layout1.add_widget(grid_medidas)
        btn_calc = Button(text='🧮 CALCULAR CÓMPUTO TÉCNICO', size_hint_y=None, height=48, background_color=(1, 0.62, 0.04, 1))
        btn_calc.bind(on_press=self.calcular)
        layout1.add_widget(btn_calc)
        self.resultado_label = Label(text='Presiona CALCULAR para ver dosificación y cómputo de materiales...', markup=True, halign='left', valign='top')
        self.resultado_label.bind(size=self.resultado_label.setter('text_size'))
        scroll1 = ScrollView()
        scroll1.add_widget(self.resultado_label)
        layout1.add_widget(scroll1)
        tab1.content = layout1
        panel.add_widget(tab1)
        tab2 = TabbedPanelHeader(text='📢 2. Modo Obra')
        layout2 = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout2.add_widget(Label(text='[b]📢 MODO OBRA / VISIBILIDAD DE CANCHA[/b]', markup=True, font_size='18sp', size_hint_y=None, height=35))
        self.giant_label = Label(text='👉 Configura tu vaciado en la Pestaña 1.', markup=True, halign='center', valign='middle', font_size='18sp')
        self.giant_label.bind(size=self.giant_label.setter('text_size'))
        scroll2 = ScrollView()
        scroll2.add_widget(self.giant_label)
        layout2.add_widget(scroll2)
        tab2.content = layout2
        panel.add_widget(tab2)
        tab3 = TabbedPanelHeader(text='💰 3. Precios (S/)')
        layout3 = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout3.add_widget(Label(text='[b]💰 Presupuesto Estimado en Soles (S/)[/b]', markup=True, font_size='18sp', size_hint_y=None, height=35))
        grid_precios = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=40)
        self.p_cemento = TextInput(text='28.50', hint_text='S/ Bolsa', multiline=False, input_filter='float')
        self.p_arena = TextInput(text='55.00', hint_text='S/ m³ Arena', multiline=False, input_filter='float')
        self.p_piedra = TextInput(text='65.00', hint_text='S/ m³ Piedra', multiline=False, input_filter='float')
        grid_precios.add_widget(self.p_cemento)
        grid_precios.add_widget(self.p_arena)
        grid_precios.add_widget(self.p_piedra)
        layout3.add_widget(grid_precios)
        btn_precio = Button(text='💵 CALCULAR PRESUPUESTO S/', size_hint_y=None, height=48, background_color=(0.2, 0.8, 0.3, 1))
        btn_precio.bind(on_press=self.calcular_presupuesto)
        layout3.add_widget(btn_precio)
        self.presupuesto_label = Label(text='Presiona CALCULAR PRESUPUESTO para ver totales en S/...', markup=True, halign='left', valign='top')
        self.presupuesto_label.bind(size=self.presupuesto_label.setter('text_size'))
        scroll3 = ScrollView()
        scroll3.add_widget(self.presupuesto_label)
        layout3.add_widget(scroll3)
        tab3.content = layout3
        panel.add_widget(tab3)
        self.total_sacos = 0.0
        self.vol_arena_m3 = 0.0
        self.vol_piedra_m3 = 0.0
        self.vol_agua_m3 = 0.0
        self.volumen_m3 = 0.0
        self.proporcion_str = '1 : 2 : 2'
        self.add_widget(panel)

    def actualizar_info_dosif(self, spinner, text):
        if "f'c 210" in text or 'Losa' in text:
            self.proporcion_str = '1 : 2 : 2'
            self.dosif_info_label.text = '[color=ff9f0a][b]👉 DOSIFICACIÓN CAPECO [1 : 2 : 2] (f\'c 210):[/b]\n1 Bolsa Cemento + 3.1 Baldes Arena + 3.1 Baldes Piedra + 1.1 Baldes Agua[/color]'
        elif "f'c 175" in text and 'Pavimentos' in text:
            self.proporcion_str = '1 : 2.5 : 2.5'
            self.dosif_info_label.text = '[color=ff9f0a][b]👉 DOSIFICACIÓN CAPECO [1 : 2.5 : 2.5] (f\'c 175):[/b]\n1 Bolsa Cemento + 3.9 Baldes Arena + 3.9 Baldes Piedra + 1.2 Baldes Agua[/color]'
        elif "f'c 175" in text and 'Hormigón' in text:
            self.proporcion_str = '1 : 5'
            self.dosif_info_label.text = '[color=ff9f0a][b]👉 DOSIFICACIÓN CAPECO [1 : 5] (Hormigón):[/b]\n1 Bolsa Cemento + 7.9 Baldes Hormigón + 1.25 Baldes Agua[/color]'
        elif 'Solados' in text or "f'c 140" in text:
            self.proporcion_str = '1 : 6'
            self.dosif_info_label.text = '[color=ff9f0a][b]👉 DOSIFICACIÓN CAPECO [1 : 6] (Solados):[/b]\n1 Bolsa Cemento + 9.4 Baldes Hormigón + 1.3 Baldes Agua[/color]'
        elif 'Ciclópeo' in text:
            self.proporcion_str = '1 : 10 + 30% P.G.'
            self.dosif_info_label.text = '[color=ff9f0a][b]👉 DOSIFICACIÓN CAPECO [1 : 10 + 30% P.G.] (Cimentación):[/b]\n1 Bolsa Cemento + 15.7 Baldes Hormigón + 30% Piedra Grande[/color]'
        else:
            self.proporcion_str = 'Manual'
            self.dosif_info_label.text = '[color=ff9f0a][b]👉 DOSIFICACIÓN PERSONALIZADA:[/b]\nDefine tus propios baldes de insumos por bolsa de cemento[/color]'

    def calcular(self, instance):
        try:
            largo = float(self.input_largo.text)
            ancho = float(self.input_ancho.text)
            espesor_m = float(self.input_espesor.text) / 100.0
            self.volumen_m3 = largo * ancho * espesor_m
            vol_desperdicio = self.volumen_m3 * 1.05
            opcion = self.tipo_spinner.text
            if "f'c 210" in opcion or 'Losa' in opcion:
                sacos_m3 = 9.73
                b_arena = 3.1
                b_piedra = 3.1
                b_agua = 1.1
            elif "f'c 175" in opcion and 'Pavimentos' in opcion:
                sacos_m3 = 8.43
                b_arena = 3.9
                b_piedra = 3.9
                b_agua = 1.2
            elif "f'c 175" in opcion and 'Hormigón' in opcion:
                sacos_m3 = 8.00
                b_arena = 7.9
                b_piedra = 0.0
                b_agua = 1.25
            elif 'Solados' in opcion or "f'c 140" in opcion:
                sacos_m3 = 7.01
                b_arena = 9.4
                b_piedra = 0.0
                b_agua = 1.3
            elif 'Ciclópeo' in opcion:
                sacos_m3 = 3.70
                b_arena = 15.7
                b_piedra = 0.0
                b_agua = 1.4
            else:
                sacos_m3 = 9.0
                b_arena = 4.0
                b_piedra = 3.0
                b_agua = 1.5
            self.total_sacos = round(vol_desperdicio * sacos_m3, 1)
            total_arena = round(self.total_sacos * b_arena, 0)
            total_piedra = round(self.total_sacos * b_piedra, 0)
            total_agua = round(self.total_sacos * b_agua, 0)
            self.vol_arena_m3 = round(total_arena * 0.018, 2)
            self.vol_piedra_m3 = round(total_piedra * 0.018, 2)
            self.vol_agua_m3 = round(total_agua * 0.018, 2)
            res = f'[b]📐 VOLUMEN VACIADO NETO:[/b] {self.volumen_m3:.2f} m³ ({vol_desperdicio:.2f} m³ con 5% desp.)\n'
            res += f'[b]🧪 PROPORCIÓN TÉCNICA CAPECO:[/b] {self.proporcion_str}\n\n'
            res += f'[b]📊 CÓMPUTO TÉCNICO DE INSUMOS FÍSICOS:[/b]\n'
            res += f'• [b]📦 Cemento Portland Tipo I:[/b] {self.total_sacos} Bolsas (42.5 kg)\n'
            res += f'• [b]🪣 Agregado Fino / Hormigón:[/b] {int(total_arena)} Baldes | ~{round(total_arena/3,1)} Buggies | {self.vol_arena_m3} m³\n'
            if b_piedra > 0:
                res += f'• [b]🪨 Agregado Grueso (Piedra 1/2"-3/4"): [/b] {int(total_piedra)} Baldes | ~{round(total_piedra/3,1)} Buggies | {self.vol_piedra_m3} m³\n'
            res += f'• [b]💧 Agua Potable / Limpia:[/b] {int(total_agua)} Baldes | ~{int(total_agua*18)} Litros\n\n'
            res += f'[b]💡 DOSIFICACIÓN TÉCNICA POR TANDA DE TROMPO (42.5 KG):[/b]\n1 Bolsa Cemento Portland + {b_arena} Baldes Agregado 1 + {b_piedra} Baldes Piedra + {b_agua} Baldes Agua'
            self.resultado_label.text = res
            giant_res = f'[b][color=ff9f0a]DOSIFICACIÓN CAPECO: {self.proporcion_str}[/color][/b]\n\n'
            giant_res += f'[b][size=36sp]🧱 {self.total_sacos} BOLSAS CEMENTO[/size][/b]\n'
            giant_res += f'[size=20sp]({self.volumen_m3:.2f} m³ Concreto)[/size]\n\n'
            giant_res += f'[b][color=34c759]💡 DOSIFICACIÓN TANDA TROMPO (1 BOLSA):[/color][/b]\n'
            giant_res += f'[size=22sp]🪣 {b_arena} BALDES AGREGADO 1\n'
            if b_piedra > 0:
                giant_res += f'🪨 {b_piedra} BALDES PIEDRA CHANCADA\n'
            giant_res += f'💧 {b_agua} BALDES AGUA LIMPIA[/size]'
            self.giant_label.text = giant_res
        except Exception as e:
            self.resultado_label.text = '[color=ff0000]Error en los datos ingresados. Revisa los números.[/color]'

    def calcular_presupuesto(self, instance):
        try:
            if self.total_sacos == 0:
                self.presupuesto_label.text = '[color=ff9900]Primero calcula los materiales en la Pestaña 1.[/color]'
                return
            p_cem = float(self.p_cemento.text)
            p_are = float(self.p_arena.text)
            p_pie = float(self.p_piedra.text)
            costo_cem = self.total_sacos * p_cem
            costo_are = self.vol_arena_m3 * p_are
            costo_pie = self.vol_piedra_m3 * p_pie
            costo_total = costo_cem + costo_are + costo_pie
            costo_m3 = costo_total / self.volumen_m3 if self.volumen_m3 > 0 else 0
            res = f'[b]💰 COSTO TOTAL ESTIMADO INSUMOS:[/b] S/ {costo_total:,.2f}\n'
            res += f'[b]📊 COSTO PROMEDIO POR m³:[/b] S/ {costo_m3:,.2f} / m³\n\n'
            res += f'[b]📋 DETALLE PRESUPUESTAL:[/b]\n'
            res += f'• Cemento Portland ({self.total_sacos} Bolsas @ S/ {p_cem}): S/ {costo_cem:,.2f}\n'
            res += f'• Agregado Fino/Hormigón ({self.vol_arena_m3} m³ @ S/ {p_are}): S/ {costo_are:,.2f}\n'
            if self.vol_piedra_m3 > 0:
                res += f'• Agregado Grueso Piedra ({self.vol_piedra_m3} m³ @ S/ {p_pie}): S/ {costo_pie:,.2f}\n'
            self.presupuesto_label.text = res
        except Exception as e:
            self.presupuesto_label.text = '[color=ff0000]Error al calcular el presupuesto. Revisa los números de precios.[/color]'

class ObraFacilApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        splash = SplashScreen(name='splash')
        main = MainScreen(name='main')
        sm.add_widget(splash)
        sm.add_widget(main)
        Clock.schedule_once(lambda dt: setattr(sm, 'current', 'main'), 2.8)
        return sm

if __name__ == '__main__':
    ObraFacilApp().run()
