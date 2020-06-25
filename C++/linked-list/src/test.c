#include "list.h"
#include <stdio.h>

// TODO: Use AceUnit or CUnit for actual unit-testing

int sq( int x ) {
  return x * x;
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

    list_clear( &list );

  return 0;
}
