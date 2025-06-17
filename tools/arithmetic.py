from langchain_core.tools import tool 
from typing import Dict, List


@tool
class Arithmetic:
    def add(value1 : float , value2 : float ):
        """
        Adds two float values and returns the result.

        Args:
            value1 (float): The first number to add.
            value2 (float): The second number to add.

        Returns:
            float: The sum of the two values.
        """

        return value1 + value2 
    
    def multiply(value1 : float , value2 : float):
        """
        Multiplies two float values and returns the result.

        Args:
            value1 (float): The first number to multiply.
            value2 (float): The second number to multiply.

        Returns:
            float: The product of the two values.
        """

        return value1 * value2 

    def calculate_total_cost(seperate_costs: List[float]) -> float:
        """
        Calculates the total cumulative cost from a list of individual expenses.

        Args:
            seperate_costs (List[float]): A list of expense amounts, such as accommodation,
            travel, tickets, attractions, or other costs associated with a trip.

        Returns:
            float: The total sum of all provided expenses.
        """
        return sum(seperate_costs)
    
    def calculate_daily_budget(daily_expenses: Dict[str, List[float]]) -> Dict[str, float]:
        """
        Calculates the total budget for each day of a trip based on specific expenses per day.

        Args:
            daily_expenses (Dict[str, List[float]]): A dictionary where each key is a day label 
            (e.g., 'Day 1', 'Day 2', etc.), and the value is a list of costs (e.g., transport, food, 
            attractions, accommodation) incurred on that day.

        Returns:
            Dict[str, float]: A dictionary mapping each day to its total budget (sum of all expenses).
        
        Example:
            Input:
                {
                    "Day 1": [100.0, 50.5, 20.0],  # hotel, food, transport
                    "Day 2": [80.0, 30.0, 25.0]    # hotel, food, entry tickets
                }

            Output:
                {
                    "Day 1": 170.5,
                    "Day 2": 135.0
                }
        """
        return {day: sum(costs) for day, costs in daily_expenses.items()}

