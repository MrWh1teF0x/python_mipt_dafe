"""
- __init__() -  инициализация экземпляра класса. Конструирует новый объект типа Vector3D 
                из трех чисел с плавающей точкой(float). По умолчанию конструирует нулевой вектор. 
                Если пользователь попытается инициализировать объект нечисловыми типами, 
                необходимо бросить исключение;  
- __repr__() -  возвращает текстовую строку: `'Vector3D(x, y, z)'`, где x, y, z - значения компонент;  
- __abs__() -   возвращает длину вектора;  
- __bool__() -  возвращает True, если вектор ненулевой, иначе - False;  
- __eq__(other) - сравнивает два вектора, возвращает True, если векторы равны покомпонентно, иначе False;  
- __neg__() -   возвращает новый объект типа Vector3D, компоненты которого равны компонентам данного вектора, 
                домноженным на минус единицу;  
- __add__(other) - складывает два вектора, возвращает новый объект типа Vector3D - сумму;  
- __sub__(other) - вычитает вектор other из данного вектора, возвращает новый объект типа Vector3D - разность;  
- __mul__(scalar) - умножение вектора на скаляр слева, возвращает новый объект типа Vector3D - произведение;  
- __rmul__(scalar) - умножение вектора на скаляр справа, возвращает новый объект типа Vector3D - произведение;  
- __truediv__(scalar) - деление вектора на скаляр, возвращает новый объект типа Vector3D - частное;  
- dot(other) - возвращает результат скалярного произведения;  
- cross(other) - возвращает векторное произведение между векторами; 

"""
from typing import Generator, Any
<<<<<<< HEAD
from numbers import Real
from math import acos


class Vector3D:
    __x: float
    __y: float
    __z: float

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        if not (isinstance(x, Real) and isinstance(y, Real) and isinstance(z, Real)):
            raise ValueError("Invalid user")
        self.__x = float(x)
        self.__y = float(y)
        self.__z = float(z)

    def __iter__(self) -> Generator[float, float, float]:
        coords = (self.x, self.y, self.z)
        return (coord for coord in coords)

    def __repr__(self) -> str:
        return f"Vector3D({self.x}, {self.y}, {self.y})"

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def __bool__(self) -> bool:
        return bool(self.__abs__())

    def __eq__(self, other: Any) -> bool:
        if not (isinstance(other, Vector3D)):
            raise ValueError("Invalid user")
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self):
        return self * (-1)

    def __add__(self, other):
        if not (isinstance(other, Vector3D)):
            raise ValueError("Invalid user")
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not (isinstance(other, Vector3D)):
            raise ValueError("Invalid user")
        return self + (-other)

    def __mul__(self, scalar: float):
        return Vector3D(scalar * self.x, scalar * self.y, scalar * self.z)

    def __rmul__(self, scalar: float):
        return self * scalar

    def __truediv__(self, scalar):
        return self * (1 / scalar)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            -(self.x * other.z - self.z * other.x),
            self.x * other.y - self.y * other.x,
        )

    def cosinus(self, other):
        return self.dot(other) / (self.__abs__() * other.__abs__())

    def distance(self, p1, p2):
        l1 = (-p1 + self).__abs__()
        l2 = (-p2 + self).__abs__()
        cosinus1 = (-p1 + self).cosinus(p2 + -p1)
        cosinus2 = (-p2 + self).cosinus(p1 + -p2)
        if l1 == 0 or l2 == 0 or (cosinus1 == 1 and cosinus2 == 1):
            return 0
        if cosinus1 <= 0 or cosinus2 <= 0:
            return min(l1, l2)
        else:
            return ((1 - cosinus1**2) ** 0.5) * l1

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def z(self) -> float:
        return self.__z


p1 = Vector3D(1, 1, 1)
p2 = Vector3D(2, 2, 2)
p3 = Vector3D(3, 3, 3)
print(p1.cosinus(p2))
print(p3.distance(p1, p2))
=======


class Vector3D:
    _x: float
    _y: float
    _z: float
    
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z: float =0
    ) -> None:
        pass
        
    def __iter__(self) -> Generator[float, None, None]:
        pass
    
    def __repr__(self) -> str:
        pass
    
    def __abs__(self) -> float:
        pass
    
    def __bool__(self) -> bool:
        pass
    
    def __eq__(self, other: Any) -> bool:    
        pass
    
    def __neg__(self):
        pass
    
    def __add__(self, other):
        pass
    
    def __sub__(self, other):
        pass
    
    def __mul__(self, scalar: float):
        pass
    
    def __rmul__(self, scalar: float):
        pass
    
    def __truediv__(self, scalar):
        pass
    
    def dot(self, other) -> float:
        pass
    
    def cross(self, other):
        pass
        
    @property
    def x(self) -> float:
        pass
    
    @property
    def y(self) -> float:
        pass
    
    @property
    def z(self) -> float:
        pass
>>>>>>> origin/main
