#include "list.h"
#include <stdio.h>

// TODO: Use AceUnit or CUnit for actual unit-testing

int sq( int x ) {
  return x * x;
}

int mult(int x, int y) {
    return x * y;
}

int plus( int x, int y ) {
  return x + y;
}

int main(void) {
    // list_append(), list_print(), list_clear()
    int N = 5;
    List list = empty_list();
    for( int i = 0; i < N; ++i ) {
        list_append( &list, i );
    }
    printf("list_append() tests: \n");
    list_print( list );

    // list_insert_before()
    printf("list_insert_before() tests: \n");
    list_insert_before(&list, -1, 4);
    list_print(list);
    list_insert_before(&list, -2, 9);
    list_print(list);
    list_insert_before(&list, 0, 0);
    list_print(list);
    list_insert_before(&list, 4, 3);
    list_print(list);

    // list_delete()
    printf("list_delete() tests: \n");
    list_delete(&list, 0);
    list_print(list);
    list_delete(&list, 9);
    list_print(list);
    list_delete(&list, 4);
    list_print(list);
    list_delete(&list, 3);
    list_print(list);

    // list_apply()
    printf("list_apply() tests: \n");
    list_apply(&list, sq);
    list_print(list);

    // list_reduce()
    printf("list_reduce() tests: \n");
    list_print(list);
    printf("list_reduce on above list and plus combiner: %d\n", list_reduce(&list, plus));
    for (int i = 10; i < 20; i += 2) {
        list_append(&list, i);
    }
    list_print(list);
    printf("list_reduce on above list and mult combiner: %d\n", list_reduce(&list, &mult));

    list_clear( &list );

  return 0;
}
