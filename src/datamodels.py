from dataclasses import dataclass

@dataclass
class OptionPosition:
    """Class representing a position in an option."""
    option_type: str  # 'call' or 'put'
    strike: float
    premium: float
    position: int = 1  # 1 for long, -1 for short
    contracts: int = 1  # Number of contracts (each represents 100 shares)

    def payoff(self, stock_price: float) -> float:
        """Calculate the payoff of the option at expiration."""
        if self.option_type.lower() == 'call':
            payoff = max(0, stock_price - self.strike)
        elif self.option_type.lower() == 'put':
            payoff = max(0, self.strike - stock_price)
        else:
            raise ValueError("Option type must be 'call' or 'put'")
        
        return self.position * (payoff - self.premium) * self.contracts * 100

@dataclass
class StockPosition:
    """Class representing a position in the underlying stock."""
    entry_price: float
    position: int = 1  # 1 for long, -1 for short
    shares: int = 100
    
    def payoff(self, stock_price: float) -> float:
        """Calculate the payoff of the stock position."""
        return self.position * (stock_price - self.entry_price) * self.shares
