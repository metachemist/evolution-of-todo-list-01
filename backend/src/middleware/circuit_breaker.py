"""
Circuit breaker pattern implementation for the Todo Evolution backend.

This module provides resilience for database connections by implementing
the circuit breaker pattern to handle failures gracefully.
"""

import asyncio
import time
from enum import Enum
from typing import Callable, Any, Optional
from functools import wraps


class CircuitBreakerState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Tripped, requests fail fast
    HALF_OPEN = "half_open" # Testing if failure condition is resolved


class CircuitBreaker:
    """
    Circuit breaker implementation to handle failures gracefully.
    """
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        """
        Initialize the circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening the circuit
            timeout: Time in seconds to wait before attempting to close the circuit
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        
        self._failure_count = 0
        self._state = CircuitBreakerState.CLOSED
        self._last_failure_time = None
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call the function with circuit breaker protection.
        
        Args:
            func: The function to call
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Result of the function call
            
        Raises:
            Exception: If the circuit is open or the function call fails
        """
        if self._state == CircuitBreakerState.OPEN:
            if time.time() - self._last_failure_time >= self.timeout:
                self._state = CircuitBreakerState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN. Request rejected.")
        
        try:
            result = func(*args, **kwargs)
            
            # Reset on success
            if self._state != CircuitBreakerState.CLOSED:
                self._state = CircuitBreakerState.CLOSED
                self._failure_count = 0
            
            return result
            
        except Exception as e:
            self._handle_error()
            raise e
    
    async def async_call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call the async function with circuit breaker protection.
        
        Args:
            func: The async function to call
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Result of the function call
            
        Raises:
            Exception: If the circuit is open or the function call fails
        """
        if self._state == CircuitBreakerState.OPEN:
            if time.time() - self._last_failure_time >= self.timeout:
                self._state = CircuitBreakerState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN. Request rejected.")
        
        try:
            result = await func(*args, **kwargs)
            
            # Reset on success
            if self._state != CircuitBreakerState.CLOSED:
                self._state = CircuitBreakerState.CLOSED
                self._failure_count = 0
            
            return result
            
        except Exception as e:
            self._handle_error()
            raise e
    
    def _handle_error(self):
        """
        Handle an error by updating the circuit breaker state.
        """
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._failure_count >= self.failure_threshold:
            self._state = CircuitBreakerState.OPEN


# Global circuit breaker instance for database connections
db_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)


def circuit_breaker_decorator(circuit_breaker: CircuitBreaker = db_circuit_breaker):
    """
    Decorator to apply circuit breaker pattern to functions.
    
    Args:
        circuit_breaker: The circuit breaker instance to use
    """
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await circuit_breaker.async_call(func, *args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return circuit_breaker.call(func, *args, **kwargs)
            return sync_wrapper
    return decorator