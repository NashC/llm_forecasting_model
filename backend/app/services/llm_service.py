import os
import json
import openai
from typing import Dict, Any, Tuple, List, Optional
import uuid
from datetime import datetime

from app.core.config import settings

# Set OpenAI API key from settings
openai.api_key = settings.OPENAI_API_KEY

# Store conversations in memory for demo
# In production, this would be stored in a database
conversations = {}


async def get_model_response(
    user_id: int,
    message: str,
    conversation_id: Optional[str] = None,
    context: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Get a response from the LLM for a user message.
    
    Args:
        user_id: The ID of the user
        message: The user's message
        conversation_id: The ID of the conversation (optional)
        context: Additional context for the conversation (optional)
        
    Returns:
        A dictionary containing the response and conversation ID
    """
    # If no conversation ID is provided, create a new conversation
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        conversations[conversation_id] = {
            "user_id": user_id,
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "context": context or {},
        }
    
    # Get the conversation or create it if it doesn't exist
    conversation = conversations.get(conversation_id)
    if not conversation:
        conversation = {
            "user_id": user_id,
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "context": context or {},
        }
        conversations[conversation_id] = conversation
    
    # Update context if provided
    if context:
        conversation["context"].update(context)
    
    # Add user message to conversation
    conversation["messages"].append({
        "role": "user",
        "content": message,
        "timestamp": datetime.now().isoformat(),
    })
    
    # Prepare messages for the API
    api_messages = []
    
    # Add system message with context
    system_message = "You are a financial forecasting assistant. You help users create, refine, and explore financial models and forecasts."
    if conversation["context"]:
        system_message += f"\n\nContext: {json.dumps(conversation['context'])}"
    
    api_messages.append({"role": "system", "content": system_message})
    
    # Add conversation history (limit to last 10 messages)
    for msg in conversation["messages"][-10:]:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=api_messages,
            temperature=0.7,
            max_tokens=800,
        )
        
        # Extract assistant message
        assistant_message = response.choices[0].message.content
        
        # Add assistant message to conversation
        conversation["messages"].append({
            "role": "assistant",
            "content": assistant_message,
            "timestamp": datetime.now().isoformat(),
        })
        
        return {
            "conversation_id": conversation_id,
            "message": assistant_message,
            "context": conversation["context"],
        }
        
    except Exception as e:
        error_message = f"Error calling OpenAI API: {str(e)}"
        print(error_message)
        
        # Add error message to conversation
        conversation["messages"].append({
            "role": "system",
            "content": error_message,
            "timestamp": datetime.now().isoformat(),
        })
        
        return {
            "conversation_id": conversation_id,
            "error": error_message,
            "context": conversation["context"],
        }


async def generate_forecast_code(
    user_id: int,
    message: str,
    model_type: str,
    historical_data: Optional[Dict] = None,
    assumptions: Optional[Dict] = None,
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate Python code for a financial forecast model.
    
    Args:
        user_id: The ID of the user
        message: The user's message describing the model
        model_type: The type of financial model to generate
        historical_data: Historical data to use for the model (optional)
        assumptions: Assumptions to use for the model (optional)
        
    Returns:
        A tuple containing (code, parameters)
    """
    # Prepare messages for the API
    api_messages = []
    
    # Add system message
    system_message = """You are a financial forecasting assistant that generates Python code.
Your task is to create a Python model based on the user's description.
The code should be well-documented, use pandas and numpy, and produce visualizations with matplotlib.
Store the model results in a 'result' dictionary.
The code should be able to run in a standalone environment with the provided parameters."""
    
    api_messages.append({"role": "system", "content": system_message})
    
    # Create prompt with model requirements
    prompt = f"""Generate a Python financial model for {model_type}.
Description: {message}

The model should:
1. Use the provided parameters or default values if not provided
2. Generate a forecast for at least 36 months
3. Include visualizations using matplotlib
4. Return results in a 'result' dictionary
5. Handle edge cases and errors gracefully
"""

    # Add historical data and assumptions if provided
    if historical_data:
        prompt += f"\nHistorical data: {json.dumps(historical_data)}"
    
    if assumptions:
        prompt += f"\nAssumptions: {json.dumps(assumptions)}"
    
    prompt += "\nPlease provide clean, well-commented Python code only, without any explanations outside the code."
    
    api_messages.append({"role": "user", "content": prompt})
    
    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=api_messages,
            temperature=0.2,
            max_tokens=2000,
        )
        
        # Extract code from response
        code = response.choices[0].message.content
        
        # Extract code from markdown if needed
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        # Generate parameters based on model type and assumptions
        if assumptions:
            parameters = assumptions
        else:
            parameters = generate_default_parameters(model_type)
        
        return code, parameters
        
    except Exception as e:
        error_message = f"Error generating model code: {str(e)}"
        print(error_message)
        
        # Return a simple template with error message
        code = f"""
# Error generating model: {str(e)}
import pandas as pd
import numpy as np

result = {{"error": "{str(e)}"}}
"""
        parameters = generate_default_parameters(model_type)
        
        return code, parameters


def generate_default_parameters(model_type: str) -> Dict[str, Any]:
    """
    Generate default parameters for a financial model based on its type.
    
    Args:
        model_type: The type of financial model
        
    Returns:
        A dictionary of default parameters
    """
    base_params = {
        "start_date": "2023-01-01",
        "periods": 36,
    }
    
    if model_type == "revenue":
        return {
            **base_params,
            "initial_customers": 100,
            "monthly_growth_rate": 0.05,
            "average_revenue_per_customer": 100,
            "churn_rate": 0.02,
        }
    
    elif model_type == "expense":
        return {
            **base_params,
            "fixed_costs": {
                "rent": 5000,
                "salaries": 20000,
                "utilities": 1000,
                "insurance": 1500,
                "other_fixed": 2000
            },
            "variable_costs": {
                "marketing": 0.10,
                "sales_commission": 0.05,
                "customer_support": 0.03,
                "other_variable": 0.02
            },
            "initial_revenue": 50000,
            "revenue_growth_rate": 0.03,
            "inflation_rate": 0.02,
        }
    
    elif model_type == "cash_flow":
        return {
            **base_params,
            "initial_cash": 100000,
            "monthly_revenue": 50000,
            "revenue_growth_rate": 0.03,
            "collection_delay": 1,
            "monthly_expenses": 40000,
            "expense_growth_rate": 0.02,
            "payment_delay": 0,
        }
    
    else:
        return {
            **base_params,
            "initial_value": 1000,
            "growth_rate": 0.02,
        } 