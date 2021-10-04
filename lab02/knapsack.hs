import Data.Char

splitToLines :: String -> [String]
splitToLines [] = []
splitToLines xs = takeWhile (/= '\n') xs : splitToLines (tail $ dropWhile (/= '\n') xs)

parse :: String -> [Integer]
parse [] = []
parse ss = (read (takeWhile isDigit ss) :: Integer) : parse (dropWhile (`elem` " \n") (dropWhile isDigit ss))

parseE :: [String] -> ([Integer], [Integer])
parseE (x:xs) = (parse x, parseValues xs)
parseE _ = ([],[])

parseD :: [String] -> ([Integer], [Integer], [Integer])
parseD (x:y:xs)= (parse x, parse y, parseValues xs)
parseD _ = ([],[],[])

parseValues :: [String] -> [Integer]
parseValues xs = [head $ parse x | x <- xs]

encrypt :: [Integer] -> Integer -> Integer
encrypt [] _ = 0
encrypt (p:pk) x
    | odd x = p + encrypt pk (x `div` 2)
    | otherwise = encrypt pk (x `div` 2)

decrypt :: Integer -> Integer -> [Integer] -> Integer -> Integer
decrypt m n sk e = d (reverse sk) 0 sum
    where
        sum = (e * (n + 1) `div` m) `mod` n
        d [] x _ = x
        d (s:sk) x sum
            | sum >= s = d sk (x*2+1) (sum-s)
            | otherwise = d sk (x*2) sum

main :: IO()
main = do
    input <- getContents
    let lines = filter (not.null) (splitToLines input)
    if head lines == "e" then do
        let (publicKey, values) = parseE $ tail lines
        mapM_ (print . encrypt publicKey) values
    else do
        let (mn, sk, values) = parseD $ tail lines
        mapM_ (print . decrypt (head mn) (head $ tail mn) sk) values