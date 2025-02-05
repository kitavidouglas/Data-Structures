package chapter_03;

import java.util.Arrays;

public class InsertionSort {

    public static void insertionSort(char[] data) {
        int arrLength = data.length;
        for (int element = 1; element < arrLength; element++) { // begin with 2nd char to check elements before
            char current = data[element]; // keep the current element
            int index = element;
            while (index > 0 && data[index - 1] > current) { // check elements to the left
                data[index] = data[index - 1]; // slide elements to the right if needed
                index--;
            }
            data[index] = current; // this is the proper position for the element to sort
        }
    }

    public static void main(String[] args) {
        char[] data = new char[] {'G', 'S', 'A', 'R', 'E', 'F', 'P', 'L', 'M', 'Z', 'B'};

        insertionSort(data);
        System.out.println(Arrays.toString(data));
    }

}
