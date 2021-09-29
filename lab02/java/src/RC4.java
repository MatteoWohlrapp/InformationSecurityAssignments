import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class Stream {

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
            if (keyAndInput[i] == -1)
                separatingKey = false;
            else if (separatingKey) {
                key[keyIndex] = keyAndInput[i];
                keyIndex++;
            } else {
                input[inputIndex] = keyAndInput[i];
                inputIndex++;
            }
        }

        return new byte[][]{key, input};
    }

    private int findKeyLength(byte[] keyAndInput){
        int keyLength = 0;

        for(int i = 0; i < keyAndInput.length; i++){
            if(keyAndInput[i] == -1)
                return keyLength;
            else
                keyLength++;
        }

        return keyLength;
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

        byte[] K = new byte[256];
    // Initialisation
        byte[] S = new byte[256];
        for(int i = 0; i < 256; i ++)
            S[i] = (byte) i;
        int j = 0;
        for(int i = 0; i < 256; i++){
            j = (j + S[i] + K[i]) % 256;
            byte temp = S[i];
            S[i] = S[j];
            S[j] = temp;
        }
        j = 0;
        int i = 0;
        byte[] encryptedMessage = new byte[input.length];

        for(int k = 0; k < input.length; k++){
            i = (i+1) %256;
            j = (j + S[i]) % 256;
            byte temp = S[i];
            S[i] = S[j];
            S[j] = temp;
            int t = (S[i] + S[j]) % 256;

            int firstByte = input[k];
            int secondByte = S[t];
            int xorByte = firstByte ^ secondByte;

            encryptedMessage[k] = (byte) xorByte;
        }

        return encryptedMessage;
    }

    public static void main(String[] args) throws IOException {
        Stream stream = new Stream();
        byte[][] keyAndInput = stream.readByteStream();
        byte[] key = keyAndInput[0];
        byte[] input = keyAndInput[1];

        byte[] crypt = stream.encryption(key, input);

        stream.writeBytes(crypt);
    }
}
