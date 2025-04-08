from typing import List, Tuple, Optional, Dict, Union
from src.datamodels import OptionPosition,StockPosition
import numpy as np
class OptionsStrategy:
    """Class representing an options trading strategy."""
    def __init__(self, name: str):
        self.name = name
        self.option_positions: List[OptionPosition] = []
        self.stock_position: Optional[StockPosition] = None
    
    def add_option(self, option_type: str, strike: float, premium: float, 
                 position: int = 1, contracts: int = 1) -> None:
        """Add an option position to the strategy."""
        self.option_positions.append(
            OptionPosition(option_type, strike, premium, position, contracts)
        )
    
    def add_stock(self, entry_price: float, position: int = 1, shares: int = 100) -> None:
        """Add a stock position to the strategy."""
        self.stock_position = StockPosition(entry_price, position, shares)
    
    def total_payoff(self, stock_price: float) -> float:
        """Calculate the total payoff of the strategy at a given stock price."""
        total = sum(option.payoff(stock_price) for option in self.option_positions)
        if self.stock_position:
            total += self.stock_position.payoff(stock_price)
        return total
    
    def initial_cost(self) -> float:
        """Calculate the initial cost of the strategy."""
        option_cost = sum(option.position * option.premium * option.contracts * 100 
                          for option in self.option_positions)
        stock_cost = 0
        if self.stock_position:
            stock_cost = self.stock_position.position * self.stock_position.entry_price * self.stock_position.shares
        return -option_cost - stock_cost if option_cost + stock_cost > 0 else abs(option_cost + stock_cost)
    
    def analyze_strategy(self, price_range: Tuple[float, float, float]) -> Dict[str, Union[float, List[float]]]:
        """
        Analyze the strategy to find key metrics.
        
        Returns:
            Dict containing:
                - 'max_profit': Maximum profit
                - 'max_loss': Maximum loss
                - 'breakeven_points': List of breakeven price points
                - 'max_profit_price': Price at which max profit occurs
                - 'max_loss_price': Price at which max loss occurs
        """
        stock_prices = np.arange(price_range[0], price_range[1], price_range[2])
        payoffs = [self.total_payoff(price) for price in stock_prices]
        
        max_profit = max(payoffs)
        max_loss = min(payoffs)
        max_profit_price = stock_prices[payoffs.index(max_profit)]
        max_loss_price = stock_prices[payoffs.index(max_loss)]
        
        # Find breakeven points
        breakeven_points = []
        for i in range(len(payoffs) - 1):
            if (payoffs[i] <= 0 and payoffs[i + 1] > 0) or (payoffs[i] >= 0 and payoffs[i + 1] < 0):
                # Linear interpolation to find breakeven
                p1, p2 = stock_prices[i], stock_prices[i + 1]
                v1, v2 = payoffs[i], payoffs[i + 1]
                if v1 != v2:  # Avoid division by zero
                    breakeven = p1 - v1 * (p2 - p1) / (v2 - v1)
                    breakeven_points.append(round(breakeven, 2))
        
        return {
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakeven_points': breakeven_points,
            'max_profit_price': max_profit_price,
            'max_loss_price': max_loss_price,
            'initial_cost': self.initial_cost()
        }
