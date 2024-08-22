import streamlit as st
st.set_page_config(layout="wide")
import plotly.express as px
import json
import pandas as pd
import plotly.graph_objs as go

def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)    
    return data

def prepare_data_iso(data, year, track, measure_type_x, measure_type_y):
    track_data = []
    years = data.keys() if year == 'All' else [year]
    for y in years:
        tracks = data[y].keys() if track == 'All' else [track]
        for t in tracks:
            if y in data and t in data[y]:
                dates = data[y][t].keys()
                for d in dates:
                    if d not in ['mean', 'std']:
                        if 'mean' in data[y][t][d] and 'std' in data[y][t][d]:  
                            if measure_type_x in [
                                'Micro', 'Macro', 'Kurtosis', 
                                'L', 'LengthRatio', 'Skewness', 
                                'ETD', 'Ra', 'MPD', 
                                'Length', 'RMS', 'Rq',                                
                            ]:
                                mean_value_x = data[y][t][d]['mean'].get(f'iso_mean_{measure_type_x}', None)
                                std_value_x = data[y][t][d]['std'].get(f'iso_mean_{measure_type_x}', None)
                            else:
                                mean_value_x = data[y][t][d]['mean'].get(f'psd_{measure_type_x}', None)
                                std_value_x = data[y][t][d]['std'].get(f'psd_{measure_type_x}', None)
                            if measure_type_y in [
                                'Micro', 'Macro', 'Kurtosis', 
                                'L', 'LengthRatio', 'Skewness', 
                                'ETD', 'Ra', 'MPD', 
                                'Length', 'RMS', 'Rq',                                
                            ]:                                
                                mean_value_y = data[y][t][d]['mean'].get(f'iso_mean_{measure_type_y}', None)
                                std_value_y = data[y][t][d]['std'].get(f'iso_mean_{measure_type_y}', None)
                            else:
                                mean_value_y = data[y][t][d]['mean'].get(f'psd_{measure_type_y}', None)
                                std_value_y = data[y][t][d]['std'].get(f'psd_{measure_type_y}', None)                                

                            if mean_value_x is not None and std_value_x is not None and mean_value_y is not None and std_value_y is not None:
                                track_data.append({
                                    'Year': y,
                                    'Track': t,
                                    'Date': d,
                                    'Mean_x': mean_value_x,
                                    'STD_x': std_value_x,
                                    'Mean_y': mean_value_y,
                                    'STD_y': std_value_y
                                })
    df = pd.DataFrame(track_data)
    df.dropna(inplace=True)
    return df.to_dict('records')

def prepare_data_psd(data, year, track, measure_type):
    track_data = []
    years = data.keys() if year == 'All' else [year]
    for y in years:
        tracks = data[y].keys() if track == 'All' else [track]
        for t in tracks:
            if y in data and t in data[y]:
                dates = data[y][t].keys()
                for d in dates:
                    if d not in ['mean', 'std']:
                        if 'mean' in data[y][t][d] and 'std' in data[y][t][d]:
                            mean_value = data[y][t][d]['mean'].get(f'psd_{measure_type}', None)
                            std_value = data[y][t][d]['std'].get(f'psd_{measure_type}', None)
                            if mean_value is not None and std_value is not None:
                                track_data.append({
                                    'Year': y,
                                    'Track': t,
                                    'Date': d,
                                    'Mean': mean_value,
                                    'STD': std_value,
                                })
    df = pd.DataFrame(track_data)
    df.dropna(inplace=True)
    return df.to_dict('records')


if __name__=='__main__':
    
    pl, pm, pr = 2, 16, 2
    plc, pmc, prc = st.columns([pl, pm, pr])
    with pmc:         

        data = load_data('outputs/surface_stats2.json')
        config = load_data('outputs/config.json')        
        st.title('Surface Statistics Analysis')


        with st.sidebar:
            st.write("Axis Range Configuration")
            custom_x_range = st.text_input("X-axis (min,max or leave blank for auto)", "")
            custom_y_range = st.text_input("Y-axis (min,max or leave blank for auto)", "")
            update_button = st.button("Update")            


        x_range = None
        y_range = None

        if update_button:
            x_range = [float(x) for x in custom_x_range.split(',')] if custom_x_range else None
            y_range = [float(y) for y in custom_y_range.split(',')] if custom_y_range else None
        

        st.write("Bivariate Analysis")     
        col1, col2, col3, col4 = st.columns(4)  
        with col1:  
            year_options = ['All'] + [str(opt) for opt in sorted(data.keys())]
            year = st.selectbox('Select Year', options=year_options)
        with col2:  
            track_options = set()
            for y, yd in data.items():
                for t, td in yd.items():
                    track_options.add(t)
            track_options = ['All'] + [str(opt) for opt in sorted(track_options)]
            track = st.selectbox('Select Track', options=track_options)
        with col3:  
            measure_type_x = st.selectbox('Select Type (X)', options=[

                'Micro', 'Macro', 'Kurtosis', 
                'L', 'LengthRatio', 'Skewness', 
                'ETD', 'Ra', 'MPD', 
                'Length', 'RMS', 'Rq',

                'H_aprox_1D', 'h0_aprox_1D', 'q0_aprox_1D', 
                'H_aprox_2D', 'h0_aprox_2D', 'q0_aprox_2D',
                'h_avg',                                 
            ])        
        with col4:  
            measure_type_y = st.selectbox('Select Type (Y)', options=[

                'Micro', 'Macro', 'Kurtosis', 
                'L', 'LengthRatio', 'Skewness', 
                'ETD', 'Ra', 'MPD', 
                'Length', 'RMS', 'Rq',

                'H_aprox_1D', 'h0_aprox_1D', 'q0_aprox_1D', 
                'H_aprox_2D', 'h0_aprox_2D', 'q0_aprox_2D',
                'h_avg',                                 
            ])        
        viz_data = prepare_data_iso(data, year, track, measure_type_x, measure_type_y)
        if viz_data:
            df_viz = pd.DataFrame(viz_data)
            df_viz['Year_Track_Date'] = df_viz['Year'] + '-' + df_viz['Track'] + '-' + df_viz['Date'].astype(str)        
            df_viz['STD_xy'] = (df_viz['STD_x'] + df_viz['STD_y'])/2      
            fig = px.scatter(
                df_viz, 
                x='Mean_x', 
                y='Mean_y', 
                size='STD_xy',  
                color='Year_Track_Date',  
                hover_name='Year_Track_Date',  
                hover_data={
                    'Year': False, 'Track': False, 'Date': False,
                    'Mean_x': ':.4f', 'Mean_y': ':.4f', 'STD_x': ':.4f', 'STD_y': ':.4f',
                    'Year_Track_Date': False, 'STD_xy': False,
                },    
                labels={
                    'Mean_x': f'{measure_type_x} (mean)',
                    'STD_x': f'{measure_type_x} (std)',                
                    'Mean_y': f'{measure_type_y} (mean)',
                    'STD_y': f'{measure_type_y} (std)',                
                    'Year_Track_Date': 'Year-Track-MMDD',                
                }, 
                title=f'{year} - {track} - {measure_type_y} vs {measure_type_x}'
            )

            if x_range:
                fig.update_xaxes(range=x_range)
            else:
                default_x_range = config.get(measure_type_x, [None, None]) 
                fig.update_xaxes(range=default_x_range)
            if y_range:
                fig.update_yaxes(range=y_range)    
            else:                
                default_y_range = config.get(measure_type_y, [None, None]) 
                fig.update_yaxes(range=default_y_range)                
            fig.update_layout(
                xaxis_title_font=dict(size=14, color='black', family='bold'),
                yaxis_title_font=dict(size=14, color='black', family='bold'),
                margin=dict(l=40, r=40, t=40, b=30)
            )
            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey'), opacity=0.8))            
            st.plotly_chart(fig, use_container_width=True)        
        else:
            st.write("No data available for the selected options.")
        

        st.write("Univariate Analysis")     
        col4, col5, col6 = st.columns(3)
        with col4:
            year_psd = st.selectbox('Select Year', options=year_options, key='year_psd')
        with col5:
            track_psd = st.selectbox('Select Track', options=track_options, key='track_psd')
        with col6:            
            measure_type_psd = st.selectbox('Select Type', options=[
                'H_aprox_1D', 'h0_aprox_1D', 'q0_aprox_1D', 
                'H_aprox_2D', 'h0_aprox_2D', 'q0_aprox_2D',
                'h_avg',                 
            ], key='measure_type_psd')
        viz_data_psd = prepare_data_psd(data, year_psd, track_psd, measure_type_psd)
        if viz_data_psd:
            df_psd = pd.DataFrame(viz_data_psd)
            df_psd['Year_Track_Date'] = df_psd['Year'] + '-' + df_psd['Track'] + '-' + df_psd['Date'].astype(str)        
            fig_psd = px.bar(
                df_psd, 
                x='Year_Track_Date', 
                y='Mean', 
                error_y='STD', 
                color='Year_Track_Date',
                color_discrete_sequence=px.colors.qualitative.Set2,
                hover_name='Year_Track_Date',  
                hover_data={
                    'Year': False, 'Track': False, 'Date': False,
                    'Mean': ':.4f', 'STD': ':.4f', 
                    'Year_Track_Date': False,
                },                    
                labels={
                    'Mean': f'{measure_type_psd} (mean)',
                    'STD': f'{measure_type_psd} (std)',                
                    'Year_Track_Date': 'Year-Track-MMDD',                
                }, 
                title=f'{year_psd} - {track_psd} - {measure_type_psd}',                
            )
            fig_psd.update_layout(
                xaxis_title_font=dict(size=14, color='black', family='bold'),
                yaxis_title_font=dict(size=14, color='black', family='bold'),
                margin=dict(l=40, r=40, t=40, b=30)
            )           
            fig_psd.update_xaxes(tickangle=-45)            
            st.plotly_chart(fig_psd, use_container_width=True)
        else:
            st.write("No data available for the selected options.")

