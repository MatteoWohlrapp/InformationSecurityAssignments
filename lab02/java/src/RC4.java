import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Arrays;

public class RC4 {

    // function returning the key at index 0 and the input message at index 1
    private byte[][] readByteStream() throws IOException {
        InputStream inputStream = System.in;
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        int next = inputStream.read();
        while (next > -1){
            byteArrayOutputStream.write(next);
            next = inputStream.read();
        }
        inputStream.close();
        byteArrayOutputStream.flush();
        byte[] array = byteArrayOutputStream.toByteArray();
        byteArrayOutputStream.close();
        return separateKeyAndInput(array);
    }

    // function separates the key and the input
    private byte[][] separateKeyAndInput(byte[] keyAndInput){
        boolean separatingKey = true;
        int keySize = findKeyLength(keyAndInput);
        byte[] key = new byte[keySize];
        byte[] input = new byte[keyAndInput.length - keySize - 1];
        int keyIndex = 0;
        int inputIndex = 0;

        for (int i = 0; i < keyAndInput.length; i ++) {

            if (separatingKey) {
                if (keyAndInput[i] == -1)
                    separatingKey = false;
                else {
                    key[keyIndex] = keyAndInput[i];
                    keyIndex++;
                }
            } else {
                input[inputIndex] = keyAndInput[i];
                inputIndex++;
            }
        }

        return new byte[][]{key, input};
    }

    private int findKeyLength(byte[] keyAndInput){
        for(int i = 0; i < keyAndInput.length; i++){
            if(keyAndInput[i] == -1)
                return i;
        }
        return 0;
    }

    // function to write the bytes to system.out
    private void writeBytes(byte[] bytes) throws IOException {
        OutputStream outputStream = System.out;
        outputStream.write(bytes);
        outputStream.flush();
        outputStream.close();
    }

    // function to en/decrypt the input with the key
    private byte[] encryption(byte[] key, byte[] input){

        // Initialisation
        short[] K = new short[256];
        short[] S = new short[256];
        for(int i = 0; i < 256; i ++) {
            S[i] = (short) i;
            K[i] = key[i % key.length];
        }

        int j = 0;
        for(int i = 0; i < 256; i++){
            j = (j + S[i] + K[i]) % 256;
            short temp = S[i];
            S[i] = S[j];
            S[j] = temp;
        }
        j = 0;
        int i = 0;

            // creating keystream
        for(int k = 0; k < input.length; k++){
            i = (i + 1) % 256;
            j = (j + S[i]) % 256;
            short temp = S[i];
            S[i] = S[j];
            S[j] = temp;
            int t = (S[i] + S[j]) % 256;
            K[k] = S[t];
        }

        // en/decrypting
        byte[] encryptedMessage = new byte[input.length];
        for(int k = 0; k < input.length; k++){

            int firstByte = input[k];
            int secondByte = K[k];
            int xorByte = firstByte ^ secondByte;

            encryptedMessage[k] = (byte) xorByte;
        }

        return encryptedMessage;
    }

    public static void main(String[] args) throws IOException {
        RC4 RC4 = new RC4();
        byte[][] keyAndInput = RC4.readByteStream();
        byte[] key = keyAndInput[0];
        byte[] input = keyAndInput[1];

        byte[] crypt = RC4.encryption(key, input);

        RC4.writeBytes(crypt);
    }
}
