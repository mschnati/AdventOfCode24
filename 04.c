#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 1000

/**
 * --- Part One ---
 * This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping 
 * other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - 
 * you need to find all of them.
 */
int find_xmas(char **data, int row_size, int col_size) {
    int count = 0;
    // Direction vectors: {row change, column change}
    int directions[8][2] = {
        {0, 1},   // Right
        {0, -1},  // Left
        {1, 0},   // Down
        {-1, 0},  // Up
        {1, 1},   // Down Right
        {-1, -1}, // Up Left
        {-1, 1},  // Up Right
        {1, -1}   // Down Left
    };
    const char *word = "XMAS";
    int word_len = strlen(word);

    for (int row = 0; row < row_size; row++) {
        for (int col = 0; col < col_size; col++) {
            if (data[row][col] == 'X') {
                // Check all eight directions
                for (int dir = 0; dir < 8; dir++) {
                    int k;
                    int new_row = row;
                    int new_col = col;
                    for (k = 1; k < word_len; k++) {
                        new_row += directions[dir][0];
                        new_col += directions[dir][1];
                        if (new_row < 0 || new_row >= row_size || new_col < 0 || new_col >= col_size)
                            break;
                        if (data[new_row][new_col] != word[k])
                            break;
                    }
                    if (k == word_len)
                        count++;
                }
            }
        }
    }
    return count;
}

/**
 * --- Part Two ---
 * it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. 
 * One way to achieve that is like this:
 *  M.S
 *  .A.
 *  M.S
 * 
 * The MAS can be in any direction, but they must be in the shape of an X.
 * Find 'A', check for M and S in opposite diagonal directions.
 */

int find_x_mas(char **data, int row_size, int col_size) {
    int count = 0;

    for (int row = 1; row < row_size - 1; row++) {
        for (int col = 1; col < col_size - 1; col++) {
            if (data[row][col] == 'A') {
                // up-left and down-right
                char ul = data[row - 1][col - 1];
                char dr = data[row + 1][col + 1];
                int diag1_match = ((ul == 'M' && dr == 'S') || (ul == 'S' && dr == 'M'));

                // up-right and down-left
                char ur = data[row - 1][col + 1];
                char dl = data[row + 1][col - 1];
                int diag2_match = ((ur == 'M' && dl == 'S') || (ur == 'S' && dl == 'M'));

                if (diag1_match && diag2_match) {
                    count++;
                }
            }
        }
    }

    return count;
}

int main() {
    char *test = "test.txt";
    char *file = "inputs/input_04.txt";
    FILE *fp;
    fp = fopen(file, "r");
    if (fp == NULL) {
        perror("Error: ");
        exit(1);
    }

    int file_size;
    fseek(fp, 0, SEEK_END);
    file_size = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    char line[MAX_LINE] = {0};
    
    // Get number of columns
    if (fgets(line, sizeof(line), fp) == NULL) {
        perror("Error: ");
        fclose(fp);
        exit(1);
    }
    int col_size = strlen(line) - 1; // Exclude newline character

    // Count number of rows
    int row_size = 1;
    while (fgets(line, sizeof(line), fp) != NULL) {
        row_size++;
    }
    rewind(fp);

    // Allocate 2D array
    char **data = malloc(sizeof(char *) * row_size);
    if (data == NULL) {
        perror("Error: Memory allocation failed\n");
        exit(1);
    }
    for (int i = 0; i < row_size; i++) {
        data[i] = malloc(sizeof(char) * col_size);
        if (data[i] == NULL) {
            perror("Error: Memory allocation failed\n");
            exit(1);
        }
    }

    // Fill the array
    for (int i = 0; i < row_size; i++) {
        if (fgets(line, sizeof(line), fp) == NULL) {
            perror("Error: ");
            fclose(fp);
            exit(1);
        }
        for (int j = 0; j < col_size; j++) {
            data[i][j] = line[j];
        }
    }

    // find "XMAS" in any direction 
    int count = find_xmas(data, row_size, col_size);

    printf("Number of XMAS found: %d\n", count);

    // find "MAS" in the shape of an X
    int count_x_mas = find_x_mas(data, row_size, col_size);

    printf("Number of X-MAS found: %d\n", count_x_mas);

    for (int i = 0; i < row_size; i++) {
        free(data[i]);
    }
    free(data);

    fclose(fp);
}