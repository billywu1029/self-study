#include <stdio.h>
#include <stdlib.h>

#define MAX_NUM_ROWS 50
#define MAX_NUM_COLS 50

typedef struct Matrix {
    int m, n;
    int rows[MAX_NUM_ROWS];
    int cols[MAX_NUM_COLS];
} Matrix;

void clear_matrix(Matrix* A) {
    for (int i = 0; i < MAX_NUM_ROWS; i++) {
        A->rows[i] = 0;
    }
    for (int j = 0; j < MAX_NUM_COLS; j++) {
        A->cols[j] = 0;
    }
}

void read_matrix(Matrix* A) {
    scanf("%d %d", &A->m, &A->n);
    for (int i = 0; i < A->m; i++) {
        for (int j = 0; j < A->n; j++) {
            int x;
            scanf("%d", &x);
            // Don't care if redundant assignment
            A->rows[i] |= x;
            A->cols[j] |= x;
        }
    }
}

void print_matrix(Matrix* A) {
    printf("Row marker array: \n");
    for (int i = 0; i < A->m; i++) {
        printf("%d ", A->rows[i]);
    }
    printf("\n");
    printf("Column marker array: \n");
    for (int j = 0; j < A->n; j++) {
        printf("%d ", A->cols[j]); 
    }
    printf("\n");
}

char* game_winner(Matrix* A) {
    static char* name[2] = {"Ashish", "Vivek"};
    // Assuming Ashish always goes first
    int turn = 1; // 1 if Ashish's turn, 0 if Vivek's
    while (1) {
        int found_row = 0;
        for (int i = 0; i < A->m; i++) {
            // Find the first available row
            if (!A->rows[i]) {
                A->rows[i] = 1;
                found_row = 1;
                break;
            }
        }
        if (!found_row) {
            return name[turn];
        }
        
        int found_col = 0;
        for (int j = 0; j < A->n; j++) {
            // Find the first available row
            if (!A->cols[j]) {
                A->cols[j] = 1;
                found_col = 1;
                break;
            }
        }
        if (!found_col) {
            return name[turn];
        }
        turn ^= 1;
    }
}

int main() {
    int num_matrices;
    scanf("%d", &num_matrices);
    Matrix matrix;

    for (int i = 0; i < num_matrices; i++) {
        clear_matrix(&matrix);
        read_matrix(&matrix);
        // print_matrix(&matrix);
        char* answer = game_winner(&matrix);
        printf("%s\n", answer);
    }
}
