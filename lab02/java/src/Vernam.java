import java.io.*;

public class Vernam {

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
        byte[] key = new byte[(keyAndInput.length - 1)/2];
        byte[] input = new byte[(keyAndInput.length - 1)/2];
        int keyIndex = 0;
        int inputIndex = 0;

        for (int i = 0; i < keyAndInput.length; i ++) {
            if (keyAndInput[i] == -1 && i == (keyAndInput.length -1) / 2)
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

    // function to en/decrypt the input with the key
    private byte[] encryption(byte[] key, byte[] input){
        byte[] encryptedMessage = new byte[input.length];

        for(int i = 0; i < input.length; i++){
            int firstByte = key[i];
            int secondByte = input[i];
            int xorByte = firstByte ^ secondByte;

            encryptedMessage[i] = (byte) xorByte;
        }

        return encryptedMessage;
    }

    // function to write the bytes to system.out
    private void writeBytes(byte[] bytes) throws IOException {
        OutputStream outputStream = System.out;
        outputStream.write(bytes);
        outputStream.flush();
        outputStream.close();
    }

    public static void main(String[] args) throws IOException {
        Vernam vernam = new Vernam();
        byte[][] keyAndInput = vernam.readByteStream();
        byte[] key = keyAndInput[0];
        byte[] input = keyAndInput[1];

        byte[] crypt = vernam.encryption(key, input);

        vernam.writeBytes(crypt);
    }
}
