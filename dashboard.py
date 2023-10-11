
#pip install dash
#pip install dash_bootstrap_components
#pip install plotly
#pip install os
#pip install datetime
#pip install dash_bootstrap_templates
#pip install pandas

from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import os
import pandas as pd
from datetime import datetime, timedelta
from datetime import date
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

# ========== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor": "top",
               "y": 0.9,
               "xanchor": "left",
               "x": 0.1,
               "title": {"text": None},
               "font": {"color": "white"},
               "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": True, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


#**************************************************************************
#*****************MONTANDO ESTRUTURA DE DADOS E ALGUNS COMPONENTES*********
#**************************************************************************
def getCSVFiles():
    # Lista para armazenar DataFrames de todos os arquivos CSV
    nomes_arquivos = []

    # Loop pelos arquivos no diretório
    for arquivo in os.listdir(os.getcwd()):
        if arquivo.endswith('.csv'):
            nomes_arquivos.append(arquivo)
    # Cria um DataFrame com a coluna "fileName"
    df_final = pd.DataFrame({'fileName': nomes_arquivos})

    return df_final

listaArquivos = getCSVFiles()

# DataFrame final que conterá todos os dados dos arquivos CSV
df_final_tudo = pd.DataFrame()
# Loop através do DataFrame com nomes de arquivo
for indice, linha in listaArquivos.iterrows():
    nome_arquivo = linha['fileName']
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

    # Lê o arquivo CSV e adiciona seu conteúdo ao DataFrame final
    df_temporario = pd.read_csv(nome_arquivo)
    df_final_tudo = pd.concat([df_final_tudo, df_temporario], ignore_index=True)

df_final_tudo = df_final_tudo.drop('id', axis=1)


def criar_dataframe_datas_ultimos_7_dias():
    # Obtém a data atual
    data_atual = datetime.now()
    # Lista para armazenar as datas dos últimos 7 dias
    datas_ultimos_7_dias = []
    datas_ultimos_7_dias.append(data_atual.strftime('%Y-%m-%d'))
    # Loop para obter as datas dos últimos 7 dias
    for i in range(7):
        data = data_atual - timedelta(days=i)
        dataFormatada = data.strftime('%Y-%m-%d')
        datas_ultimos_7_dias.append(dataFormatada)
    # Cria um DataFrame com as datas
    df = pd.DataFrame({'Data': datas_ultimos_7_dias})
    return df

ultimos7DiasDF = criar_dataframe_datas_ultimos_7_dias()

df_semana = df_final_tudo[df_final_tudo['data'].isin(ultimos7DiasDF['Data'])]


dataHojeFormatada = datetime.now().strftime('%Y-%m-%d')
dfHjFiltro = pd.DataFrame({'Data': [dataHojeFormatada]})
df_hoje = df_final_tudo[df_final_tudo['data'].isin(dfHjFiltro['Data'])]


df_hoje['Quantidade'] = 1
df_semana['Quantidade'] = 1
figHoje = px.bar(df_hoje, x="classicacao", y="Quantidade", color="classicacao", barmode="group",width=900, height=400)
figSemana = px.bar(df_semana, x="classicacao", y="Quantidade", color="data", barmode="group",width=1500, height=400)

options_tipos_audio = list(df_final_tudo['classicacao'].unique())

listaAudiosDia = list(df_hoje.hora)




#**************************************************************************
#**********************************MONTANDO LAYOUT*************************
#**************************************************************************
app.layout = dbc.Container(children=[
    # Layout
    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Listening House")
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-stethoscope', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Base code from Asimov Academy", style={'font-size': '90%','margin-top': '30px'})
                        ])
                    ], style={}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://asimov.academy/", target="_blank")
                    ], style={'margin-top': '0px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Resumo diário')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='grafico_audios_dia',
                                figure=figHoje,
                                className='dbc',
                                config=config_graph,
                                style={'font-size': '90%','margin-top': '0px'}
                            )


                            #dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o tipo de audio'),
                            dbc.RadioItems(
                                id="radio_tipo_audio",
                                options=options_tipos_audio,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                                style={'margin': '1px'}
                            ),
                            html.Div([
                                html.P(''),

                            ]),
                            dcc.DatePickerSingle(
                                id='data_choicer',
                                min_date_allowed=date(2023, 8, 5),
                                max_date_allowed=date(2100, 9, 19),
                                initial_visible_month=date(datetime.now().year, datetime.now().month, datetime.now().day),
                                date=date(datetime.now().year, datetime.now().month, datetime.now().day),
                                display_format='Y-MM-DD'
                            ),
                            html.Div([
                                html.P(''),
                                html.P('Selecione seu audio abaixo.')
                            ]),
                            dcc.Dropdown(options=listaAudiosDia, value='Audios', id='dropdown_lista_audios'),
                            html.Div([
                                html.P(''),

                            ]),
                            html.Audio(id='audioPlayer',src='', controls=True),
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin': '2px'}),

    html.Div([
        html.P(''),

    ]),
    # Row 2
    dbc.Row([
        dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Legend('Resumo semanal'),
                            dcc.Graph(id='graphSemanal', className='dbc', config=config_graph,figure=figSemana)
                        ])
                    ], style=tab_card)
                ]),
        ])
    ], className='my-auto', style={'margin': '2px'}),



], fluid=True, style={'height': '100vh'})



#**************************************************************************
#**********************************CALLBACKS*******************************
#**************************************************************************

@app.callback(
    Output('dropdown_lista_audios', 'options'),
    Input('data_choicer', 'date'),
    Input('radio_tipo_audio', 'value')
)
def update_output(dateStr,tipo):
    dateObj = datetime.strptime(dateStr, '%Y-%m-%d').date()
    dataFormatada = dateObj.strftime('%Y-%m-%d')
    dfFiltroData = pd.DataFrame({'Data': [dataFormatada]})
    dfFiltroclassicacao = pd.DataFrame({'classicacao': [tipo]})

    df_data_filtrado = df_final_tudo[df_final_tudo['data'].isin(dfFiltroData['Data'])]
    df_data_filtrado = df_data_filtrado[df_data_filtrado['classicacao'].isin(dfFiltroclassicacao['classicacao'])]
    listaAudiosFiltrado = list(df_data_filtrado.hora)
    return  listaAudiosFiltrado


@app.callback(
    Output('audioPlayer', 'src'),
    Input('dropdown_lista_audios', 'value'),
    Input('data_choicer', 'date'),
    Input('radio_tipo_audio', 'value'),
)
def dropdown_lista_audios(audioHourSelected,data,tipo):
    horaFormatada = str(audioHourSelected.split(".")[0]).replace(":","-")
    pathFile = "assets/" + data+ "/" + data+"_"+horaFormatada +"_"+tipo+".wav"
    return pathFile




# Run server
if __name__ == '__main__':
    app.run_server(debug=False)