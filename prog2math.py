#!/usr/bin/env python3
import json
import argparse
import sys
import inspect
import base64
from typing import Union

# Logo
LOGO = base64.b64decode(b'CiAgICw6OFAqKioqKioqKioqKipeXl5eXl5eXl5eXl5eXl5eXl5eWWIuCiAgaiY6OC46JzouOic6LjonOi46JzouLjonOi46JzouOic6LjonOi4lfGkuCiAgPyY6ODouPz8/Pz8/Pz8/Pz8/PzpkYjo/Pz8/Pz8/Pz8/Pz8/LjolfHxpLgogID8mOjguOj8/JSUlJSUlJSUlJTpkPz9iOiUlJSUlJSUlJSUhPzouJXx8fHwKICBJJiYmYi4/PyUlIT8/Pz8/PzpkPy4uP2I6Pz8/Pz8/PyUlIT8uOiUhfCF8ICAg4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKWiOKVlyAg4paI4paI4paI4paI4paI4paI4pWXICDilojilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKVlyAgIOKWiOKWiOKWiOKVlyDilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4pWXICDilojilojilZcKICBFJjg6Sjg6PyUlIT8/Pz8/OmQ/LicnLj9iOj8/Pz8/PyUlIT86LiV8fHwhICAg4paI4paI4pWU4pWQ4pWQ4paI4paI4pWX4paI4paI4pWU4pWQ4pWQ4paI4paI4pWX4paI4paI4pWU4pWQ4pWQ4pWQ4paI4paI4pWX4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWdIOKVmuKVkOKVkOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKWiOKWiOKVlyDilojilojilojilojilZHilojilojilZTilZDilZDilojilojilZfilZrilZDilZDilojilojilZTilZDilZDilZ3ilojilojilZEgIOKWiOKWiOKVkQogIGwlJSVQJzo/JSUhPz8/PzpkPy4nOjonLj9iOj8/Pz8/JSUhPy46JXwhfHwgICDilojilojilojilojilojilojilZTilZ3ilojilojilojilojilojilojilZTilZ3ilojilojilZEgICDilojilojilZHilojilojilZEgIOKWiOKWiOKWiOKVlyDilojilojilojilojilojilZTilZ3ilojilojilZTilojilojilojilojilZTilojilojilZHilojilojilojilojilojilojilojilZEgICDilojilojilZEgICDilojilojilojilojilojilojilojilZEKICA6Ky4rLjo/PyUlIT8/PzpkPy4nOjo6OicuP2I6Pz8/PyUlIT86LiUhfDp8ICAg4paI4paI4pWU4pWQ4pWQ4pWQ4pWdIOKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKVkOKVnSDilojilojilZHilZrilojilojilZTilZ3ilojilojilZHilojilojilZTilZDilZDilojilojilZEgICDilojilojilZEgICDilojilojilZTilZDilZDilojilojilZEKICA/JjolOi4/PyUlIT8/OmQ/Lic6Ojo6OjonLj9iOj8/PyUlIT8uOiUhfCEhICAg4paI4paI4pWRICAgICDilojilojilZEgIOKWiOKWiOKVkeKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVl+KWiOKWiOKVkSDilZrilZDilZ0g4paI4paI4pWR4paI4paI4pWRICDilojilojilZEgICDilojilojilZEgICDilojilojilZEgIOKWiOKWiOKVkQogID8mOiUuOj8/JSUhPzpkPy4nOjo6Ojo6OjonLj9iOj8/JSUhPzouJXwhfHwgICDilZrilZDilZ0gICAgIOKVmuKVkOKVnSAg4pWa4pWQ4pWdIOKVmuKVkOKVkOKVkOKVkOKVkOKVnSAg4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWdIOKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVneKVmuKVkOKVnSAgICAg4pWa4pWQ4pWd4pWa4pWQ4pWdICDilZrilZDilZ0gICDilZrilZDilZ0gICDilZrilZDilZ0gIOKVmuKVkOKVnQogID8mOiU6Lj8/JSUhOmQ/Lic6O3Nzc3Nzczo6Jy4/Yjo/JSUhPy46JXx8fHwKICA/ODolLjo/PyUlOmpZLHNQKiJgICBfX2AiKj9zLllsOiUlIT86LiUhOiEhICAgICAgICAgICAgVHVybnMgcHJvZ3JhbW1pbmcgaW50byBtYXRobWF0aWNhbCBmb3JtdWxhZSAoTGFUZXgpCiAgPzg6JTouPz8lOmpZcyIgLi4gOmRQOjo6IC4uICJzWWw6JSE/LjolfCF8fCAgICAgICAgICAgICAgICAgQnkgSm9uYXRoYW4gQmFyIE9yICgiSkJPIiksIEB5b195b195b19qYm8KICA/ODolLjo/PzpqeGwgLjo6IDoqOiAgOjo6IDo6LiBKeGw6IT86LiV8fCEhICAgICAgICAgICAgICAgICAgICAgaHR0cHM6Ly95by15by15by1qYm8uZ2l0aHViLmlvCiAgPzg6JS46PzpqWS5gWWI6OiBgOjo6Ojo6JyA6OmRQYC5ZbDo/Ljo/ISE6fAogIEkmJiZiLjpqWS4nOi4iPz9zLi4gICAgLi5zPz8iLjonLllsOjouPyF8ISEKICBFJjg6Sjg6WS4nOjo6Oi4uYGAiKioqKiJgYC4uOjo6OicuWWwuOj8hOiF8CiAgbCUlJVAnVi46Li4uLi4uLjo6Oi4uLi46OjouLi4uLi4uOi5WOy4/ISEhIQogID8rLis6ZGJzc3Nzc3Nzc3MrKysrKysrKysrKysrKysrKysrJSU6PyF8OiEKICA/JS4lLjo/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz86Lj8hOiF8CiAgPyUuJSc6LjonOi46JzouOic6LjonOi46JzouOic6LjonOi46Jzo/ISE6IQogIDolLllhYWFhYWFzc3Nzc3Nzc3JycnJycnJycnJyKysrKysrKysrZiF8IXwKICAgYFknOjo7Ozs6Ojo6Ozs7Ojo6Ojs7Ozs7Ojo6Ojo6Ojo7Ozs7Ozo6OnwhCiAgICAgYCIqOjo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6JwoK').decode()

class LatexExpr(object):
    """
        Latex expression.
    """

    def __init__(self, expression:Union[str, float, int]):
        """
            Creates an instance.
        """

        # Save the expression
        self._expression = str(expression)

    def get_expression(self) -> str:
        """
            Gets the expression.
        """

        # Return the expression
        return self._expression

    def __str__(self) -> str:
        """
            Returns the expression.
        """

        # Return the expression
        return self.get_expression()

    @staticmethod
    def compose(a:'LatexExpr', b:'LatexExpr') -> 'LatexExpr':
        """
            Composes expressions.
        """
    
        # Create the expression
        return fr'{a}\left({b}\right)'

class Indicator(LatexExpr):
    """
        An indicator of a condition, should yield 0 or 1 only.
    """

    def __init__(self, expression:str):
        """
            Creates an instance.
            Since there is no true way of enforcing expression argument would be a true indicator (i.e. yields either 0 or 1 exclusively) - it is simply an assumption.
        """

        # Call super
        super().__init__(expression)

    @staticmethod
    def logical_and(*indicators:list['Indicator']) -> 'Indicator':
        """
            Creates a new indicator that indicates the logical and of other indicators.
        """

        # Validations
        assert len(indicators) > 0, Exception('Must provide at least one indicator')

        # Create a new indicator by means of multiplication
        return Indicator(''.join([ fr'\left({ind}\right)' for ind in indicators ]))

    @staticmethod
    def logical_not(indicator:'Indicator') -> 'Indicator':
        """
            Creates a new indicator that indicates the negation of the given indicator.
        """

        # Yield a new indicator
        return Indicator(fr'1-\left({indicator}\right)')

    @staticmethod
    def logical_or(*indicators:list['Indicator']) -> 'Indicator':
        """
            Creates a new indicator that indicates the logical or of other indicators.
        """

        # Validations
        assert len(indicators) > 0, Exception('Must provide at least one indicator')

        # Create a new indicator by de Morgan's laws
        return Indicator.logical_not(Indicator.logical_and(*map(Indicator.logical_not, indicators)))

    @staticmethod
    def are_not_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for inequality of two expressions.
        """

        # Use the arctan function and normalize it to indicate inequality
        return Indicator(r'\left\lceil\frac{4\arctan^2{\left(' + f'{a}-{b}' + r'\right)}}{\pi^2}\right\rceil')

    @staticmethod
    def are_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator of equality of two expressions.
        """

        # Use the inequality indicator
        return Indicator.logical_not(Indicator.are_not_equal(a, b))

    @staticmethod
    def is_non_negative(a:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for the given expression being non-negative.
        """

        # Check equality of the expression and its absolute value
        abs_val_expr = LatexExpr(r'\sqrt{' + fr'\left({a}\right)^2' + r'}')
        return Indicator.are_equal(abs_val_expr, a)

    @staticmethod
    def less_than_or_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator of a <= b.
        """

        # Use the non-negativity indicator
        return Indicator.is_non_negative(LatexExpr(f'{b}-{a}'))

    @staticmethod
    def less_than(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for a < b.
        """

        # Use the negation of a >= b
        return Indicator.logical_not(Indicator.less_than_or_equal(b, a))

    @staticmethod
    def bigger_than_or_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for a >= b.
        """

        # Switch roles
        return Indicator.less_than_or_equal(b, a)

    @staticmethod
    def bigger_than(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for a > b.
        """

        # Switch roles
        return Indicator.less_than(b, a)

    @staticmethod
    def is_integer(a:LatexExpr) -> 'Indicator':
        """
            Indicates whether the given expression is an integer.
        """

        # Use the cosine function's period
        return Indicator(fr'\left\lfloor\left(\cos\left(\pi {a}\right)\right)^2\right\rfloor')

    @staticmethod
    def is_natural(a:LatexExpr, include_zero:bool=False) -> 'Indicator':
        """
            Indicates whether the given expression is a natural number (starting from either 0 or 1 as indicated).
        """

        # Use integer checking along a comparison
        natural_cond = Indicator.is_non_negative(a) if include_zero else Indicator.bigger_than(a, LatexExpr(0))
        return Indicator.logical_and(Indicator.is_integer(a), natural_cond)

    @staticmethod
    def divides(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Indicates if a divides b, assuming it is not zero.
        """

        # Use the integer indicator
        return Indicator.is_integer(LatexExpr(r'\frac{' + str(b) + '}{' + str(a) + '}'))

    @staticmethod
    def does_not_divide(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Indicates if a doesn't divide a, assuming it is not zero.
        """

        # Negate the division indicator
        return Indicator.logical_not(Indicator.divides(a, b))

    def get_mod(a:LatexExpr, b:LatexExpr) -> LatexExpr:
        """
            Calculates a % b, which is a (mod b), assuming b is not 0.
        """

        # Use the floor function
        return fr'{a} - {b}\left\lfloor\frac' + '{' + str(a) + '}{' + str(b) + r'}\right\rfloor'

    @staticmethod
    def is_prime_divisors(a:LatexExpr, index_letter:str='i') -> 'Indicator':
        """
            Indicates if the given number is prime by means of iterating its divisors.
        """

        # Validations
        assert len(index_letter) == 1, Exception(f'Invalid index letter "{index_letter}"')
        assert index_letter.islower(), Exception(f'Invalid index letter "{index_letter}"')

        # Loop through all numbers between 2 and (a-1) and check if any of them divide our candidate
        prod_expr = LatexExpr(r'\prod_{' + index_letter + '=2}^{' + f'{a}-1' + '}\left(' + str(Indicator.does_not_divide(LatexExpr(index_letter), a))  +  r'\right)')
        return Indicator.logical_and(Indicator.is_natural(a), Indicator.is_natural(prod_expr, include_zero=False))

    @staticmethod
    def is_prime_wilson(a:LatexExpr) -> 'Indicator':
        """
            Indicates if the given number is prime by means of Wilson's theorem.
        """

        # Use Wilson's theorem with integer testing alongside making sure our candidate is strictly greater than one
        return Indicator.logical_and(Indicator.less_than(1, a), Indicator.is_integer(LatexExpr(r'\frac{\left(' + str(a) + r'-1\right)!+1}{' + str(a) + '}')))

    @staticmethod
    def get_post_decimal_point_digit(a:LatexExpr, b:LatexExpr) -> LatexExpr:
        """
            Gets the b-th digit of the expression "a" after the decimal point.
        """

        # Use the floor function
        return LatexExpr(r'\left\lfloor10^' + f'{b} {a}' + r'\right\rfloor - 10\left\lfloor10^{' + str(b) + '-1} ' + str(a) + r'\right\rfloor')

    @staticmethod
    def all_in_range(lo:LatexExpr, hi:LatexExpr, indicator:'Indicator', index_letter:str='k') -> 'Indicator':
        """
            Indicates if all integers in the given range yield true for the given indicator.
        """

        # Return as a product
        return Indicator(r'\sum_{' + f'{index_letter}={lo}' + '}^{' + str(hi) + r'}\left(' + str(indicator) + r'\right)')
    
    @staticmethod
    def count_in_range(lo:LatexExpr, hi:LatexExpr, indicator:'Indicator', index_letter:str='k') -> LatexExpr:
        """
            Creates an expression of how many numbers in the integer range indicate true.
        """

        # Return as a sum
        return LatexExpr(r'\sum_{' + f'{index_letter}={lo}' + '}^{' + str(hi) + r'}\left(' + str(indicator) + r'\right)')

    @staticmethod
    def is_range_at_least_exp(lo:LatexExpr, hi:LatexExpr, n:LatexExpr, indicator:'Indicator', index_letter:str='k') -> 'Indicator':
        """
            Uses exponentiation to indicate whether the given range has at least n elements that yield true.
        """

        # Yield
        return r'\left\lfloor\sqrt[{n}]{\frac{' + str(n) + '}{' + str(Indicator.count_in_range(lo, hi, indicator, index_letter)) + r'}}\right\rfloor'

class LoadingUtils(object):
    """
        Loading utilities.
    """

    # Cache that maps method names to class methods
    _METHOD_NAMES_MAPPING = None

    # Maps class names to classes
    _CLASS_NAMES_MAPPING = None

    @classmethod
    def _add_to_cache(cls, method_name:str, method_obj:object) -> None:
        """
            Adds the given method name to the cache.
        """

        # Validate uniqueness and add
        prev_method_obj = cls._METHOD_NAMES_MAPPING.get(method_name, None)
        if prev_method_obj == method_obj:
            return
        assert prev_method_obj is None, Exception(f'Method "{method_name}" is not unique')
        cls._METHOD_NAMES_MAPPING[method_name] = method_obj

    @classmethod
    def _build_cache(cls) -> None:
        """
            Builds the cache that maps method names and class names to methods and classes.
        """

        # Empty caches
        cls._METHOD_NAMES_MAPPING = {}
        cls._CLASS_NAMES_MAPPING = {}
        
        # Get all members in the module
        for class_name, class_obj in inspect.getmembers(sys.modules[__name__], predicate=inspect.isclass):

            # Only take subclasses of LatexExpr
            if not issubclass(class_obj, LatexExpr):
                continue

            # Map the class name to the object
            assert class_name not in cls._CLASS_NAMES_MAPPING, Exception(f'Class "{class_name}" is not unique')
            cls._CLASS_NAMES_MAPPING[class_name] = class_obj

            # Get all functions
            for func_name, func_obj in inspect.getmembers(class_obj, predicate=inspect.isfunction):

                # Skip abstract
                if inspect.isabstract(func_obj):
                    continue

                # Handle constructors
                if func_name == '__init__':
                    cls._add_to_cache(class_name, func_obj)
                    continue

                # Skip private or protected ones
                if func_name.startswith('_'):
                    continue

                # Skip instance methods
                if 'self' in inspect.signature(func_obj).parameters:
                    continue

                # Add to cache
                cls._add_to_cache(func_name, func_obj)
                continue

    @classmethod
    def _get_class_from_name(cls, class_name:str, throw_if_not_found:bool=True) -> object:
        """
            Gets a class from its name.
        """

        # Fill the cache if necessary
        if cls._CLASS_NAMES_MAPPING is None:
            cls._build_cache()

        # Get the result from the mapping
        result = cls._CLASS_NAMES_MAPPING.get(class_name, None)
        if throw_if_not_found:
            assert result is not None, Exception(f'Class "{class_name}" not found')
        return result

    @classmethod
    def _get_method_from_name(cls, method_name:str, throw_if_not_found:bool=True) -> object:
        """
            Gets a method from its name.
        """

        # Fill the cache if necessary
        if cls._METHOD_NAMES_MAPPING is None:
            cls._build_cache()

        # Get the result from the mapping
        result = cls._METHOD_NAMES_MAPPING.get(method_name, None)
        if throw_if_not_found:
            assert result is not None, Exception(f'Method "{method_name}" not found')
        return result

    @classmethod
    def create_expr_by_reflection(cls, expr_method_name:str, expr_method_args:dict[str, object]) -> LatexExpr:
        """
            Creates an expression instance by the means of reflection.
        """

        # Get the method object
        method = cls._get_method_from_name(expr_method_name)
        
        # Build keyword arguments
        kwds = {}
        for arg_name, arg_val in expr_method_args.items():

            # Validate argument exists
            assert arg_name in inspect.signature(method).parameters, Exception(f'Argument "{arg_name}" not found for method "{expr_method_name}"')

            # Resolve annotation
            annotation = None
            if isinstance(inspect.signature(method).parameters[arg_name].annotation, str):
                annotation = cls._get_class_from_name(inspect.signature(method).parameters[arg_name].annotation, throw_if_not_found=False)
            elif issubclass(inspect.signature(method).parameters[arg_name].annotation, LatexExpr):
                annotation = inspect.signature(method).parameters[arg_name].annotation

            # Handle recursive types
            if annotation is not None:

                # Strings or numbers can be instanciated
                if isinstance(arg_val, float) or isinstance(arg_val, int) or isinstance(arg_val, str):
                    kwds[arg_name] = LatexExpr(arg_val)
                    continue

                # Handle compound types recursively
                assert isinstance(arg_val, dict), Exception(f'Argument "{arg_name}" for method "{expr_method_name}" must be a compound type')
                assert len(arg_val) == 1, Exception(f'Argument "{arg_name}" for method "{expr_method_name}" must have a single entry')
                key = list(arg_val.keys())[0]
                assert arg_name not in kwds, Exception(f'Argument "{arg_name}" for method "{expr_method_name}" is not unique')
                kwds[arg_name] = LoadingUtils.create_expr_by_reflection(key, arg_val[key])
                continue
            
            # Handle simple types
            assert arg_name not in kwds, Exception(f'Argument "{arg_name}" for method "{expr_method_name}" is not unique')
            kwds[arg_name] = arg_val

        # Run the method
        return method(**kwds)

def main() -> None:
    """
        Main routine.
    """

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jsonfile', dest='json_file', type=str, help='The input JSON file path.', required=True)
    parser.add_argument('-q', '--quiet', dest='quiet',action='store_true', help='Quiet mode that does not show logo and other info.')
    args = parser.parse_args()

    # Print logo
    if not args.quiet:
        print(LOGO)

    # Catch all errors
    try:

        # Open the JSON file
        with open(args.json_file, 'r') as fp:
            input_dict = json.load(fp)

        # Validate input dictionary has one element and create that expression
        assert len(input_dict) == 1, Exception(f'Input JSON "{args.json_file}" must have a single entry')
        key = list(input_dict.keys())[0]
        expr = LoadingUtils.create_expr_by_reflection(key, input_dict[key])

        # Write expression
        print(str(expr))

        # Indicate success
        sys.exit(0)

    except Exception as ex:

        # Print exception unless we are in quiet mode
        if not args.quiet:
            print(f'Error: {exception}')
        
        # Return -1
        sys.exit(-1)

if __name__ == '__main__':
    main()

