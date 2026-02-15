"""
AuraGrid Capstone: Renewable Grid Performance Monitoring System

Author: Khaled Eissa
Date: February 13, 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os
from datetime import datetime


class GridDataProcessor:
    """
    Class to process sensor data from renewable energy sources.
    Handles data loading, cleaning, transformation, and aggregation.
    """
    
    def __init__(self, filepath):
        """Initialize with file path."""
        self.filepath = filepath
        self.dataframe = None
        self.weekly_data = None
        self.top5_sources = []
        print("Grid Data Processor Initialized")
        print("Target file:", filepath)
    
    def read_data(self):
        """Read sensor data from CSV file with exception handling."""
        print("\nSTEP 1: Reading data from file")
        
        try:
            self.dataframe = pd.read_csv(self.filepath)
            
            required_columns = ['Time', 'Source_ID', 'Power_Output', 'Efficiency_Factor']
            missing_columns = [col for col in required_columns if col not in self.dataframe.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            print(f"Loaded {len(self.dataframe):,} records")
            print(f"Columns: {list(self.dataframe.columns)}")
            print(f"Date range: {self.dataframe['Time'].min()} to {self.dataframe['Time'].max()}")
            print(f"Unique sources: {self.dataframe['Source_ID'].nunique()}")
            
            return self.dataframe
            
        except FileNotFoundError:
            print(f"ERROR: File not found - {self.filepath}")
            print("Please check the file path and try again.")
            raise FileNotFoundError(f"Sensor data file not found: {self.filepath}")
            
        except pd.errors.EmptyDataError:
            print(f"ERROR: File is empty - {self.filepath}")
            raise IOError(f"The file {self.filepath} contains no data")
            
        except pd.errors.ParserError as e:
            print(f"ERROR: Failed to parse CSV file")
            print(f"Details: {e}")
            raise IOError(f"Corrupted or invalid CSV format in {self.filepath}")
            
        except Exception as e:
            print(f"ERROR: Unexpected error - {type(e).__name__}: {e}")
            raise IOError(f"Failed to read {self.filepath}: {e}")
    
    def clean_data(self):
        """Clean data by converting datetime and removing null values."""
        print("\nSTEP 2: Cleaning data")
        
        if self.dataframe is None:
            raise ValueError("No data loaded. Call read_data() first.")
        
        original_count = len(self.dataframe)
        
        print("Converting Time column to datetime...")
        self.dataframe['Time'] = pd.to_datetime(self.dataframe['Time'], errors='coerce')
        
        invalid_dates = self.dataframe['Time'].isna().sum()
        if invalid_dates > 0:
            print(f"Warning: {invalid_dates} invalid dates found and removed")
            self.dataframe = self.dataframe.dropna(subset=['Time'])
        
        print("Removing rows with null Power_Output values...")
        null_power_before = self.dataframe['Power_Output'].isna().sum()
        self.dataframe = self.dataframe.dropna(subset=['Power_Output'])
        self.dataframe = self.dataframe.reset_index(drop=True)
        
        rows_removed = original_count - len(self.dataframe)
        retention_rate = (len(self.dataframe) / original_count) * 100
        
        print(f"Cleaning complete:")
        print(f"  Original records: {original_count:,}")
        print(f"  Records removed: {rows_removed:,}")
        print(f"  Records retained: {len(self.dataframe):,} ({retention_rate:.1f}%)")
        print(f"  Null Power_Output removed: {null_power_before}")
        
        return self.dataframe
    
    def transform_data(self):
        """Calculate efficiency ratio using vectorized operations."""
        print("\nSTEP 3: Transforming data")
        
        if self.dataframe is None:
            raise ValueError("No data loaded. Call read_data() and clean_data() first.")
        
        print("Calculating Efficiency_Ratio = Power_Output / Efficiency_Factor...")
        
        self.dataframe['Efficiency_Ratio'] = (
            self.dataframe['Power_Output'] / 
            self.dataframe['Efficiency_Factor']
        )
        
        infinite_count = np.isinf(self.dataframe['Efficiency_Ratio']).sum()
        if infinite_count > 0:
            print(f"Warning: {infinite_count} infinite values detected")
            self.dataframe['Efficiency_Ratio'].replace([np.inf, -np.inf], np.nan, inplace=True)
        
        valid_ratios = self.dataframe['Efficiency_Ratio'].notna().sum()
        avg_ratio = self.dataframe['Efficiency_Ratio'].mean()
        
        print(f"Transformation complete:")
        print(f"  Valid Efficiency_Ratio values: {valid_ratios:,}")
        print(f"  Average Efficiency_Ratio: {avg_ratio:.2f}")
        print(f"  Min: {self.dataframe['Efficiency_Ratio'].min():.2f}")
        print(f"  Max: {self.dataframe['Efficiency_Ratio'].max():.2f}")
        
        return self.dataframe
    
    def aggregate_weekly_output(self):
        """Aggregate power output to weekly totals by Source_ID."""
        print("\nSTEP 4: Aggregating to weekly data")
        
        if self.dataframe is None:
            raise ValueError("No data loaded. Complete previous steps first.")
        
        df_agg = self.dataframe.copy()
        df_agg = df_agg.sort_values('Time')
        
        print("Grouping by Source_ID and resampling to weekly...")
        df_agg.set_index('Time', inplace=True)
        
        weekly = df_agg.groupby('Source_ID').resample('W')['Power_Output'].sum()
        self.weekly_data = weekly.reset_index()
        
        print("Identifying top 5 sources...")
        total_by_source = self.weekly_data.groupby('Source_ID')['Power_Output'].sum()
        total_by_source = total_by_source.sort_values(ascending=False)
        self.top5_sources = total_by_source.head(5).index.tolist()
        
        total_weeks = self.weekly_data['Time'].nunique()
        total_sources = self.weekly_data['Source_ID'].nunique()
        overall_weekly_total = self.weekly_data['Power_Output'].sum()
        
        print(f"Aggregation complete:")
        print(f"  Total weeks: {total_weeks}")
        print(f"  Sources tracked: {total_sources}")
        print(f"  Total power output: {overall_weekly_total:,.2f} kWh")
        print(f"\nTop 5 Producing Sources:")
        for i, source in enumerate(self.top5_sources, 1):
            source_total = total_by_source.loc[source]
            print(f"  {i}. {source}: {source_total:,.2f} kWh")
        
        return self.weekly_data, self.top5_sources
    
    def get_summary_statistics(self):
        """Get summary statistics for processed data."""
        if self.dataframe is None:
            return {}
        
        stats = {
            'total_records': len(self.dataframe),
            'unique_sources': self.dataframe['Source_ID'].nunique(),
            'date_range_start': self.dataframe['Time'].min(),
            'date_range_end': self.dataframe['Time'].max(),
            'total_power_output': self.dataframe['Power_Output'].sum(),
            'avg_power_output': self.dataframe['Power_Output'].mean(),
            'avg_efficiency_factor': self.dataframe['Efficiency_Factor'].mean(),
            'avg_efficiency_ratio': self.dataframe['Efficiency_Ratio'].mean(),
        }
        
        return stats


class ReportGenerator:
    """
    Class to generate visual reports for grid performance.
    Creates Matplotlib and Plotly visualizations.
    """
    
    def __init__(self, dataframe, weekly_data, top5_sources):
        """Initialize with processed data."""
        self.dataframe = dataframe
        self.weekly_data = weekly_data
        self.top5_sources = top5_sources
        
        os.makedirs('reports', exist_ok=True)
        
        print("\nReport Generator Initialized")
        print(f"Data records: {len(dataframe):,}")
        print(f"Weekly data points: {len(weekly_data):,}")
        print(f"Top sources: {len(top5_sources)}")
    
    def generate_matplotlib_report(self):
        """Generate static line plot showing weekly power output trends."""
        print("\nSTEP 5: Creating Matplotlib visualization")
        
        plt.figure(figsize=(14, 7))
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        
        print("Plotting top 5 sources...")
        for idx, source in enumerate(self.top5_sources):
            source_data = self.weekly_data[
                self.weekly_data['Source_ID'] == source
            ].sort_values('Time')
            
            plt.plot(
                source_data['Time'], 
                source_data['Power_Output'],
                marker='o', 
                label=source,
                linewidth=2.5,
                markersize=6,
                color=colors[idx % len(colors)],
                alpha=0.8
            )
            
            print(f"  Plotted {source}: {len(source_data)} weeks")
        
        plt.xlabel('Week', fontsize=13, fontweight='bold')
        plt.ylabel('Total Power Output (kWh)', fontsize=13, fontweight='bold')
        plt.title('Weekly Power Output Trends - Top 5 Renewable Sources', 
                  fontsize=15, fontweight='bold', pad=20)
        
        plt.legend(
            loc='upper left', 
            fontsize=11,
            frameon=True,
            shadow=True,
            title='Source ID',
            title_fontsize=12
        )
        
        plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        output_path = 'reports/weekly_output_trend.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\nStatic report saved to: {output_path}")
        
        return output_path
    
    def generate_plotly_dashboard(self):
        """Generate interactive scatter plot for efficiency analysis."""
        print("\nSTEP 6: Creating Plotly dashboard")
        
        plot_data = self.dataframe.reset_index(drop=True)
        
        print("Creating interactive scatter plot...")
        
        fig = px.scatter(
            plot_data,
            x='Efficiency_Factor',
            y='Power_Output',
            color='Source_ID',
            hover_data={
                'Source_ID': True,
                'Time': True,
                'Power_Output': ':.2f',
                'Efficiency_Factor': ':.4f',
                'Efficiency_Ratio': ':.2f'
            },
            title='Efficiency Factor vs Power Output - Interactive Dashboard',
            labels={
                'Efficiency_Factor': 'Efficiency Factor',
                'Power_Output': 'Power Output (kWh)',
                'Source_ID': 'Source ID'
            },
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig.update_layout(
            font=dict(size=12, family='Arial'),
            title_font_size=16,
            title_font_family='Arial Black',
            title_x=0.5,
            hovermode='closest',
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            legend=dict(
                title=dict(text='Source ID', font=dict(size=13)),
                orientation='v',
                yanchor='top',
                y=1,
                xanchor='left',
                x=1.02
            ),
            margin=dict(l=80, r=150, t=100, b=80)
        )
        
        fig.update_xaxes(
            title_font=dict(size=13, family='Arial Black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
        fig.update_yaxes(
            title_font=dict(size=13, family='Arial Black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
        
        fig.update_traces(
            marker=dict(size=6, opacity=0.7, line=dict(width=0.5, color='white'))
        )
        
        output_path = 'reports/efficiency_dashboard.html'
        fig.write_html(
            output_path,
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['lasso2d', 'select2d']
            }
        )
        
        print(f"\nInteractive dashboard saved to: {output_path}")
        print(f"Data points: {len(plot_data):,}")
        
        return output_path


def main():
    """Main function to run the grid optimizer pipeline."""
    print("\nAuraGrid Capstone Project")
    print("Grid Performance Monitoring System")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Student: Khaled Eissa\n")
    
    try:
        input_file = 'sensor_data.csv'
        
        print("PHASE 1: Data Processing")
        
        processor = GridDataProcessor(input_file)
        processor.read_data()
        processor.clean_data()
        processor.transform_data()
        weekly_data, top5_sources = processor.aggregate_weekly_output()
        stats = processor.get_summary_statistics()
        
        print("\nData processing completed")
        
        print("\nPHASE 2: Generating Reports")
        
        reporter = ReportGenerator(processor.dataframe, weekly_data, top5_sources)
        matplotlib_output = reporter.generate_matplotlib_report()
        plotly_output = reporter.generate_plotly_dashboard()
        
        print("\nAll reports generated")
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total records processed: {stats['total_records']:,}")
        print(f"Unique sources: {stats['unique_sources']}")
        print(f"Period: {stats['date_range_start'].strftime('%Y-%m-%d')} to {stats['date_range_end'].strftime('%Y-%m-%d')}")
        print(f"Total power output: {stats['total_power_output']:,.2f} kWh")
        print(f"Average power: {stats['avg_power_output']:.2f} kWh")
        print(f"Average efficiency factor: {stats['avg_efficiency_factor']:.4f}")
        print(f"Average efficiency ratio: {stats['avg_efficiency_ratio']:.2f}")
        print(f"\nOutput files:")
        print(f"  1. {matplotlib_output}")
        print(f"  2. {plotly_output}")
        print("="*60)
        
        print("\nGrid optimizer completed successfully")
        
        return 0
        
    except FileNotFoundError as e:
        print("\nERROR: Input file not found")
        print(f"Details: {e}")
        print("Please check that sensor_data.csv exists")
        return 1
        
    except IOError as e:
        print("\nERROR: File I/O error")
        print(f"Details: {e}")
        return 1
        
    except Exception as e:
        print("\nERROR: Unexpected error occurred")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
