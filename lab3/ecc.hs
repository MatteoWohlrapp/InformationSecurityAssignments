import Data.Char
import Data.List

parseLine :: String -> [Integer]
parseLine [] = []
parseLine (s:ss)
    | isDigit s = (read (takeWhile isDigit (s:ss)) :: Integer) : parseLine (dropWhile (`elem` "() \n") (dropWhile isDigit (s:ss)))
    | otherwise = parseLine (dropWhile (`elem` "() \n") ss)

double :: Num c => [c] -> (c, c)
double (a:b:_) = (a, b)
double _ = (-1, -1)

triple :: Num c => [c] -> (c, c, c)
triple (a:b:c:_) = (a, b, c)
triple _ = (-1, -1, -1)

binary :: Integer -> [Integer]
binary n = reverse (b n)
    where
        b n
            | n == 0 = []
            | even n = 0 : b (n `div` 2)
            | otherwise = 1 : b (n `div` 2)

apply :: (a -> a) -> a -> a -> Integer -> a
apply f x base n
    | n == 0 = base
    | n == 1 = x
    | otherwise = f (apply f x base (n-1))

modularInverse :: Integer -> Integer -> Integer
modularInverse m n
    | f m n 1 0 < 0 = n + f m n 1 0
    | otherwise = f m n 1 0
    where
        f m n o p
            | m == 0 = p
            | otherwise = f (n-q*m) m (p-q*o) o
                where q = n `div` m

pointAddition :: (Integer, Integer) -> (Integer, Integer) -> Integer -> Integer -> (Integer, Integer)
pointAddition (x1, y1) (x2, y2) a p
    | x2 < x1 = pointAddition (x2, y2) (x1, y1) a p
    | (x1, y1) == (p, p) = (x2, y2)
    | (x2, y2) == (p, p) = (x1, y1)
    | inv == 0 = (p, p) --infinity notation
    | otherwise = (x3, y3)
    where
        x3 = (m^2 - x1 - x2) `mod` p
        y3 = (m * (x1-x3) - y1) `mod` p
        m
            | x1 == x2 && y1 == y2 = (3 * x1^2 + a) * inv
            | otherwise = (y2 - y1) * inv
        inv
            | x1 == x2 && y1 == y2 = modularInverse (2*y1) p
            | otherwise = modularInverse (x2 - x1) p

pointDouble ::  (Integer, Integer) -> Integer -> Integer -> (Integer, Integer)
pointDouble xy = pointAddition xy xy

pointMultiplication :: Integer -> (Integer, Integer) -> Integer -> Integer -> (Integer, Integer)
pointMultiplication z xy a p = foldr (\x y -> pointAddition x y a p) (p,p) (replicate (fromIntegral z) xy)

pointMultiplication2 :: Integer -> (Integer, Integer) -> Integer -> Integer -> (Integer, Integer)
pointMultiplication2 z xy a p
    | z == 1 = xy
    | even z = pointMultiplication (z `div` 2) (pointDouble xy a p) a p
    | otherwise = pointAddition xy (pointMultiplication (z-1) xy a p) a p

pointMultiplication3 :: Integer -> (Integer, Integer) -> Integer -> Integer -> (Integer, Integer)
pointMultiplication3 z xy a p = foldl (\i j -> pointAddition i j a p) (p,p) (map (apply (\l -> pointDouble l a p) xy (p,p)) powers)
    where
        bin = binary z
        powers = zipWith (\x y -> y * 2^x) [0..length bin-1] bin

main :: IO()
main = do
    line1 <- getLine
    line2 <- getLine
    line3 <- getLine
    let xy = double $ parseLine line1
    let (a, b, p) = triple $ parseLine line2
    let (m, n) = double $ parseLine line3
    let (x',y') = pointMultiplication m (pointMultiplication n xy a p) a p
    let s = '(': show x' ++ ", " ++ show y' ++ ")"
    putStrLn s