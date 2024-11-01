from typing import Union

class LatexExpr(object):
    """
        Latex expression.
    """

    def __init__(self, expression:Union[str, float]):
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
        return Indicator(fr'\left\lfloor\cos^2\left(\pi {a}\right)\right\rfloor')

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
        return LocalExpr(r'\left\lfloor10^' + f'{b} {a}' + r'\right\rfloor - 10\left\lfloor10^{' + str(b) + '-1} ' + str(a) + r'\right\rfloor')

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

print(Indicator.count_in_range(LatexExpr(1), LatexExpr(10), Indicator.is_prime_wilson(LatexExpr('n'))))
