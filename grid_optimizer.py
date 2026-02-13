import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os
from datetime import datetime


class GridDataProcessor:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataframe = None
        self.weekly_data = None
        self.top5_sources = []
    
    def read_data(self):
        try:
            self.dataframe = pd.read_csv(self.filepath)
            required = ['Time', 'Source_ID', 'Power_Output', 'Efficiency_Factor']
            missing = [col for col in required if col not in self.dataframe.columns]
            if missing:
                raise ValueError(f"Missing columns: {missing}")
            return self.dataframe
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except Exception as e:
            raise IOError(f"Error reading file: {e}")
    
    def clean_data(self):
        if self.dataframe is None:
            raise ValueError("No data loaded")
        
        self.dataframe['Time'] = pd.to_datetime(self.dataframe['Time'], errors='coerce')
        self.dataframe = self.dataframe.dropna(subset=['Time', 'Power_Output'])
        self.dataframe = self.dataframe.reset_index(drop=True)
        return self.dataframe
    
    def transform_data(self):
        if self.dataframe is None:
            raise ValueError("No data loaded")
        
        self.dataframe['Efficiency_Ratio'] = self.dataframe['Power_Output'] / self.dataframe['Efficiency_Factor']
        self.dataframe['Efficiency_Ratio'].replace([np.inf, -np.inf], np.nan, inplace=True)
        return self.dataframe
    
    def aggregate_weekly_output(self):
        if self.dataframe is None:
            raise ValueError("No data loaded")
        
        df = self.dataframe.copy().sort_values('Time')
        df.set_index('Time', inplace=True)
        
        weekly = df.groupby('Source_ID').resample('W')['Power_Output'].sum()
        self.weekly_data = weekly.reset_index()
        
        totals = self.weekly_data.groupby('Source_ID')['Power_Output'].sum().sort_values(ascending=False)
        self.top5_sources = totals.head(5).index.tolist()
        
        return self.weekly_data, self.top5_sources


class ReportGenerator:
    
    def __init__(self, dataframe, weekly_data, top5_sources):
        self.dataframe = dataframe
        self.weekly_data = weekly_data
        self.top5_sources = top5_sources
        os.makedirs('reports', exist_ok=True)
    
    def generate_matplotlib_report(self):
        plt.figure(figsize=(14, 7))
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        
        for idx, source in enumerate(self.top5_sources):
            data = self.weekly_data[self.weekly_data['Source_ID'] == source].sort_values('Time')
            plt.plot(data['Time'], data['Power_Output'], marker='o', label=source,
                    linewidth=2.5, markersize=6, color=colors[idx], alpha=0.8)
        
        plt.xlabel('Week', fontsize=13, fontweight='bold')
        plt.ylabel('Total Power Output (kWh)', fontsize=13, fontweight='bold')
        plt.title('Weekly Power Output Trends - Top 5 Sources', fontsize=15, fontweight='bold', pad=20)
        plt.legend(loc='upper left', fontsize=11, frameon=True, shadow=True, title='Source ID')
        plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        plt.savefig('reports/weekly_output_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        return 'reports/weekly_output_trend.png'
    
    def generate_plotly_dashboard(self):
        data = self.dataframe.reset_index(drop=True)
        
        fig = px.scatter(data, x='Efficiency_Factor', y='Power_Output', color='Source_ID',
                        hover_data={'Source_ID': True, 'Time': True, 'Power_Output': ':.2f',
                                  'Efficiency_Factor': ':.4f', 'Efficiency_Ratio': ':.2f'},
                        title='Efficiency Factor vs Power Output',
                        labels={'Efficiency_Factor': 'Efficiency Factor',
                               'Power_Output': 'Power Output (kWh)', 'Source_ID': 'Source ID'},
                        color_discrete_sequence=px.colors.qualitative.Bold)
        
        fig.update_layout(font=dict(size=12), title_font_size=16, title_x=0.5, hovermode='closest',
                         plot_bgcolor='rgba(240, 240, 240, 0.5)',
                         legend=dict(title=dict(text='Source ID'), orientation='v',
                                   yanchor='top', y=1, xanchor='left', x=1.02),
                         margin=dict(l=80, r=150, t=100, b=80))
        
        fig.update_xaxes(title_font=dict(size=13), showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(title_font=dict(size=13), showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_traces(marker=dict(size=6, opacity=0.7, line=dict(width=0.5, color='white')))
        
        fig.write_html('reports/efficiency_dashboard.html',
                      config={'displayModeBar': True, 'displaylogo': False,
                             'modeBarButtonsToRemove': ['lasso2d', 'select2d']})
        return 'reports/efficiency_dashboard.html'


def main():
    try:
        processor = GridDataProcessor('sensor_data.csv')
        processor.read_data()
        processor.clean_data()
        processor.transform_data()
        weekly_data, top5 = processor.aggregate_weekly_output()
        
        reporter = ReportGenerator(processor.dataframe, weekly_data, top5)
        reporter.generate_matplotlib_report()
        reporter.generate_plotly_dashboard()
        
        print("Processing complete")
        print(f"Records: {len(processor.dataframe)}")
        print(f"Sources: {processor.dataframe['Source_ID'].nunique()}")
        print(f"Total output: {processor.dataframe['Power_Output'].sum():,.2f} kWh")
        
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
