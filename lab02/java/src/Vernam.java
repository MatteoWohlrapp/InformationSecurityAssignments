import java.io.*;
import java.util.Arrays;

public class VernamCipher {

    // function returning the key at index 0 and the input message at index 1
    private byte[][] readByteStream() throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        int next = br.read();
        while (next > -1){
            byteArrayOutputStream.write(next);
            next = br.read();
        }
        byteArrayOutputStream.flush();
        byte[] array = byteArrayOutputStream.toByteArray();
        byteArrayOutputStream.close();
        return separateKeyAndInput(array);
    }

    // function separates the key and the input
    private byte[][] separateKeyAndInput(byte[] keyAndInput){
        boolean separatingKey = true;
        byte[] key = new byte[(keyAndInput.length - 1)/2];
        byte[] input = new byte[(keyAndInput.length - 1)/2];
        int keyIndex = 0;
        int inputIndex = 0;

        for (byte b : keyAndInput) {
            if (b == (byte) 0xff)
                separatingKey = false;
            else if (separatingKey) {
                key[keyIndex] = b;
                keyIndex++;
            } else {
                input[inputIndex] = b;
                inputIndex++;
            }
        }

        return new byte[][]{key, input};
    }

    private byte[] cryption(byte[] key, byte[] input){
        byte[] transformedMessage = new byte[input.length];

        for(int i = 0; i < input.length; i++){
            int firstByte = key[i];
            int secondByte = input[i];
            int xorByte = firstByte ^ secondByte;

            transformedMessage[i] = (byte) xorByte;
        }

        return transformedMessage;
    }

    public static void main(String[] args) throws IOException {
        VernamCipher vernamCipher = new VernamCipher();
        byte[][] keyAndInput = vernamCipher.readByteStream();
        byte[] key = keyAndInput[0];
        byte[] input = keyAndInput[1];

        System.out.println(Arrays.toString(input));
    }
}
