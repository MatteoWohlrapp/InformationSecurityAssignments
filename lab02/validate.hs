import Data.Char

privateKeyInvalid = -1
publicKeyInvalid = 0
valid = 1

parse :: String -> [Integer]
parse [] = []
parse ss = (read (takeWhile isDigit ss) :: Integer) : parse (dropWhile (`elem` " \n") (dropWhile isDigit ss))

validation :: [Integer] -> [Integer] -> [Integer] -> Integer
validation (m:n:xs) privateKey publicKey
    | not $ validatePrivateKey m n privateKey = privateKeyInvalid
    | length privateKey /= length publicKey || any (\(x,y) -> y /= (x * m) `mod` n) (zip privateKey publicKey) = publicKeyInvalid
    | otherwise = valid
validation _ _ _ = privateKeyInvalid

validatePrivateKey :: Integer -> Integer -> [Integer] -> Bool
validatePrivateKey m n privateKey = gcd m n == 1 && n > last sK && isSuperIncreasing privateKey sK
    where
        sK = superIncreasing 0 privateKey
        superIncreasing sum [] = [sum]
        superIncreasing sum (x:xs) = sum + x : superIncreasing (sum + x) xs
        isSuperIncreasing pk = isi (tail pk)
        isi [] _ = True
        isi (p:pks) (s:sks) = p > s && isi pks sks
        isi _ _ = False

main :: IO()
main = do
    mn <- getLine
    privateKey <- getLine
    publicKey <- getLine
    print (validation (parse mn) (parse privateKey) (parse publicKey))