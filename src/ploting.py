from typing import List, Tuple
from src.option_strategy import OptionsStrategy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
# def visualise(
#     strategies: List[OptionsStrategy], 
#     price_range: Tuple[float, float, float],
#     title: str = "Options Strategy P&L Comparison",
#     show_breakeven: bool = True,
#     show_max_values: bool = True
# ) -> go.Figure:
#     """
#     Plot P&L charts for multiple options strategies using Plotly.
    
#     Args:
#         strategies: List of OptionsStrategy objects
#         price_range: Tuple of (min_price, max_price, step)
#         title: Chart title
#         show_breakeven: Whether to highlight breakeven points
#         show_max_values: Whether to show max profit/loss
        
#     Returns:
#         Plotly Figure object
#     """
#     stock_prices = np.arange(price_range[0], price_range[1], price_range[2])
    
#     # Create plot with custom dimensions
#     fig = go.Figure()
    
#     # Color palette
#     colors = [
#         '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
#         '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
#     ]
    
#     # Plot each strategy and analyze metrics
#     for i, strategy in enumerate(strategies):
#         # Get payoffs and analyze strategy
#         payoffs = [strategy.total_payoff(price) for price in stock_prices]
#         analysis = strategy.analyze_strategy(price_range)
        
#         # Format currency values for hover info
#         hovertemplate = (
#             f"<b>{strategy.name}</b><br>" +
#             "Stock Price: $%{x:.2f}<br>" +
#             "P&L: $%{y:.2f}<br>" +
#             f"Initial Cost: ${analysis['initial_cost']:.2f}<br>" +
#             f"Max Profit: ${analysis['max_profit']:.2f}<br>" +
#             f"Max Loss: ${analysis['max_loss']:.2f}"
#         )
        
#         # Add strategy line
#         color = colors[i % len(colors)]
#         fig.add_trace(go.Scatter(
#             x=stock_prices,
#             y=payoffs,
#             mode='lines',
#             name=strategy.name,
#             line=dict(color=color, width=3),
#             hovertemplate=hovertemplate
#         ))
        
#         # Handle breakeven points if requested
#         if show_breakeven and analysis['breakeven_points']:
#             for be_point in analysis['breakeven_points']:
#                 # Add breakeven markers
#                 fig.add_trace(go.Scatter(
#                     x=[be_point],
#                     y=[0],
#                     mode='markers',
#                     marker=dict(size=10, color=color, symbol='circle'),
#                     name=f"{strategy.name} BE: ${be_point:.2f}",
#                     showlegend=False,
#                     hovertemplate=f"Breakeven: ${be_point:.2f}"
#                 ))
                
#                 # Add breakeven annotations
#                 fig.add_annotation(
#                     x=be_point,
#                     y=0,
#                     text=f"BE: ${be_point:.2f}",
#                     showarrow=True,
#                     arrowhead=2,
#                     arrowcolor=color,
#                     arrowsize=1,
#                     arrowwidth=2,
#                     ax=0,
#                     ay=40,
#                     font=dict(color=color),
#                     bordercolor=color,
#                     borderwidth=2,
#                     borderpad=4,
#                     bgcolor='white',
#                     opacity=0.8
#                 )
        
#         # Add max profit/loss markers if requested
#         if show_max_values:
#             # Max profit marker
#             fig.add_trace(go.Scatter(
#                 x=[analysis['max_profit_price']],
#                 y=[analysis['max_profit']],
#                 mode='markers',
#                 marker=dict(size=12, color=color, symbol='star', line=dict(width=2, color='white')),
#                 name=f"{strategy.name} Max Profit",
#                 showlegend=False,
#                 hovertemplate=f"Max Profit: ${analysis['max_profit']:.2f}<br>at Stock Price: ${analysis['max_profit_price']:.2f}"
#             ))
            
#             # Max loss marker (if not at extremes of the range)
#             if analysis['max_loss_price'] > price_range[0] + price_range[2] and analysis['max_loss_price'] < price_range[1] - price_range[2]:
#                 fig.add_trace(go.Scatter(
#                     x=[analysis['max_loss_price']],
#                     y=[analysis['max_loss']],
#                     mode='markers',
#                     marker=dict(size=12, color=color, symbol='x', line=dict(width=2, color='white')),
#                     name=f"{strategy.name} Max Loss",
#                     showlegend=False,
#                     hovertemplate=f"Max Loss: ${analysis['max_loss']:.2f}<br>at Stock Price: ${analysis['max_loss_price']:.2f}"
#                 ))
    
#     # Add zero line
#     fig.add_shape(
#         type="line",
#         x0=price_range[0],
#         y0=0,
#         x1=price_range[1],
#         y1=0,
#         line=dict(color="black", width=2, dash="dash")
#     )
    
#     # Improve layout
#     fig.update_layout(
#         title=dict(
#             text=title,
#             font=dict(size=24)
#         ),
#         xaxis=dict(
#             title="Stock Price at Expiration",
#             tickprefix="$",
#             gridcolor='lightgrey'
#         ),
#         yaxis=dict(
#             title="Profit/Loss",
#             tickprefix="$",
#             tickformat=",.0f",
#             gridcolor='lightgrey',
#             zerolinecolor='black',
#             zerolinewidth=2
#         ),
#         legend=dict(
#             x=0.01,
#             y=0.99,
#             bgcolor='rgba(255, 255, 255, 0.8)',
#             bordercolor='lightgrey',
#             borderwidth=1
#         ),
#         hoverlabel=dict(
#             bgcolor="white",
#             font_size=14,
#             font_family="Arial"
#         ),
#         hovermode="closest",
#         template="plotly_white",
#         height=700,
#         margin=dict(t=100)
#     )
    
#     # Add summary table at the top
#     strategy_summaries = []
#     for strategy in strategies:
#         analysis = strategy.analyze_strategy(price_range)
#         strategy_summaries.append({
#             'Strategy': strategy.name,
#             'Initial Cost': f"${analysis['initial_cost']:.2f}",
#             'Max Profit': f"${analysis['max_profit']:.2f}",
#             'Max Loss': f"${analysis['max_loss']:.2f}",
#             'Breakeven Points': ", ".join([f"${bp:.2f}" for bp in analysis['breakeven_points']]) if analysis['breakeven_points'] else "N/A"
#         })
    
#     summary_df = pd.DataFrame(strategy_summaries)
    
#     # Create a table for the summary
#     table = go.Figure(data=[go.Table(
#         header=dict(
#             values=list(summary_df.columns),
#             fill_color='paleturquoise',
#             align='left',
#             font=dict(size=14)
#         ),
#         cells=dict(
#             values=[summary_df[col] for col in summary_df.columns],
#             fill_color='lavender',
#             align='left',
#             font=dict(size=13)
#         ),
#         columnwidth=[0.8, 0.7, 0.7, 0.7, 1.5]
#     )])
    
#     return fig,table

def plot_strategy_pnl_plotly(
    strategies: List[OptionsStrategy], 
    price_range: Tuple[float, float, float],
    title: str = "Options Strategy P&L Comparison",
    show_breakeven: bool = True,
    show_max_values: bool = True
) -> go.Figure:
    """
    Plot P&L charts for multiple options strategies using Plotly with a summary table.
    
    Args:
        strategies: List of OptionsStrategy objects
        price_range: Tuple of (min_price, max_price, step)
        title: Chart title
        show_breakeven: Whether to highlight breakeven points
        show_max_values: Whether to show max profit/loss
        
    Returns:
        Plotly Figure object with subplot containing both chart and table
    """
    stock_prices = np.arange(price_range[0], price_range[1], price_range[2])
    
    # Create subplot layout with 2 rows - chart on top, table below
    fig = make_subplots(
        rows=2, 
        cols=1,
        row_heights=[0.8, 0.2],  # 80% chart, 20% table
        vertical_spacing=0.1,
        specs=[
            [{"type": "scatter"}],  # For the chart
            [{"type": "table"}]     # For the table
        ],
        subplot_titles=[title, "Strategy Summary"]
    )
    
    # Color palette
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    # Prepare data for summary table
    strategy_summaries = []
    
    # Plot each strategy and analyze metrics
    for i, strategy in enumerate(strategies):
        # Get payoffs and analyze strategy
        payoffs = [strategy.total_payoff(price) for price in stock_prices]
        analysis = strategy.analyze_strategy(price_range)
        
        # Populate summary data for table
        strategy_summaries.append({
            'Strategy': strategy.name,
            'Initial Cost': f"${analysis['initial_cost']:.2f}",
            'Max Profit': f"${analysis['max_profit']:.2f}",
            'Max Loss': f"${analysis['max_loss']:.2f}",
            'Breakeven Points': ", ".join([f"${bp:.2f}" for bp in analysis['breakeven_points']]) if analysis['breakeven_points'] else "N/A"
        })
        
        # Format currency values for hover info
        hovertemplate = (
            f"<b>{strategy.name}</b><br>" +
            "Stock Price: $%{x:.2f}<br>" +
            "P&L: $%{y:.2f}<br>" +
            f"Initial Cost: ${analysis['initial_cost']:.2f}<br>" +
            f"Max Profit: ${analysis['max_profit']:.2f}<br>" +
            f"Max Loss: ${analysis['max_loss']:.2f}"
        )
        
        # Add strategy line to chart subplot (row 1)
        color = colors[i % len(colors)]
        fig.add_trace(
            go.Scatter(
                x=stock_prices,
                y=payoffs,
                mode='lines',
                name=strategy.name,
                line=dict(color=color, width=3),
                hovertemplate=hovertemplate
            ),
            row=1, col=1
        )
        
        # Handle breakeven points if requested
        if show_breakeven and analysis['breakeven_points']:
            for be_point in analysis['breakeven_points']:
                # Add breakeven markers
                fig.add_trace(
                    go.Scatter(
                        x=[be_point],
                        y=[0],
                        mode='markers',
                        marker=dict(size=10, color=color, symbol='circle'),
                        name=f"{strategy.name} BE: ${be_point:.2f}",
                        showlegend=False,
                        hovertemplate=f"Breakeven: ${be_point:.2f}"
                    ),
                    row=1, col=1
                )
                
                # Add breakeven annotations
                fig.add_annotation(
                    x=be_point,
                    y=0,
                    text=f"BE: ${be_point:.2f}",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=color,
                    arrowsize=1,
                    arrowwidth=2,
                    ax=0,
                    ay=40,
                    font=dict(color=color),
                    bordercolor=color,
                    borderwidth=2,
                    borderpad=4,
                    bgcolor='white',
                    opacity=0.8,
                    row=1, col=1
                )
        
        # Add max profit/loss markers if requested
        if show_max_values:
            # Max profit marker
            fig.add_trace(
                go.Scatter(
                    x=[analysis['max_profit_price']],
                    y=[analysis['max_profit']],
                    mode='markers',
                    marker=dict(size=12, color=color, symbol='star', line=dict(width=2, color='white')),
                    name=f"{strategy.name} Max Profit",
                    showlegend=False,
                    hovertemplate=f"Max Profit: ${analysis['max_profit']:.2f}<br>at Stock Price: ${analysis['max_profit_price']:.2f}"
                ),
                row=1, col=1
            )
            
            # Max loss marker (if not at extremes of the range)
            if analysis['max_loss_price'] > price_range[0] + price_range[2] and analysis['max_loss_price'] < price_range[1] - price_range[2]:
                fig.add_trace(
                    go.Scatter(
                        x=[analysis['max_loss_price']],
                        y=[analysis['max_loss']],
                        mode='markers',
                        marker=dict(size=12, color=color, symbol='x', line=dict(width=2, color='white')),
                        name=f"{strategy.name} Max Loss",
                        showlegend=False,
                        hovertemplate=f"Max Loss: ${analysis['max_loss']:.2f}<br>at Stock Price: ${analysis['max_loss_price']:.2f}"
                    ),
                    row=1, col=1
                )
    
    # Add zero line to chart
    fig.add_shape(
        type="line",
        x0=price_range[0],
        y0=0,
        x1=price_range[1],
        y1=0,
        line=dict(color="black", width=2, dash="dash"),
        row=1, col=1
    )
    
    # Convert summary data to DataFrame
    summary_df = pd.DataFrame(strategy_summaries)
    
    # Add table to second subplot
    fig.add_trace(
        go.Table(
            header=dict(
                values=list(summary_df.columns),
                fill_color='rgba(30, 144, 255, 0.8)',  # Dodger blue
                align='left',
                font=dict(color='white', size=14)
            ),
            cells=dict(
                values=[summary_df[col] for col in summary_df.columns],
                fill_color=[['rgba(240, 240, 240, 0.8)' if i % 2 == 0 else 'rgba(220, 220, 220, 0.8)' 
                            for i in range(len(summary_df))] for _ in range(len(summary_df.columns))],
                align='left',
                font=dict(size=13)
            ),
            columnwidth=[0.8, 0.7, 0.7, 0.7, 1.5]
        ),
        row=2, col=1
    )
    
    # Improve layout
    fig.update_layout(
        xaxis=dict(
            title="Stock Price at Expiration",
            tickprefix="$",
            gridcolor='lightgrey'
        ),
        yaxis=dict(
            title="Profit/Loss",
            tickprefix="$",
            tickformat=",.0f",
            gridcolor='lightgrey',
            zerolinecolor='black',
            zerolinewidth=2
        ),
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='lightgrey',
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        ),
        hovermode="closest",
        template="plotly_white",
        height=900,  # Increased height to accommodate the table
        margin=dict(t=60, b=20, l=60, r=60)
    )
    
    # Update subplot titles font size
    fig.update_annotations(font_size=18)
    
    return fig