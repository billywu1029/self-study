#include "list.h"

#include <stdio.h>
#include <stdlib.h>

struct List_node_s {
  List_node *next;
  int value;
};

List empty_list( void ) {
  return (List) { .length = 0, .front = NULL };
}

// Allocate memory for a single List_node
List_node* create_node( int value ) {
  List_node *new_node = malloc( sizeof( List_node ) );
  new_node->value = value;
  new_node->next = NULL;
  return new_node;
}

void list_append( List *list, int value ) {
  /* Function to append a new node containing 'value'
   * to the end of List *list. For example,
   * applied to { 5 -> 10 } as
   * list_append( list, 9 ); results in
   * { 5 -> 10 -> 9 }
   *
   * TODO: Currently naive implementation of iterating all the way to the end of the LL to append
   */
    List_node *curr_node = list->front;
    if (!curr_node) {
      list->front = create_node(value);
    } else {
        while( curr_node->next != NULL ) {
            curr_node = curr_node->next;
        }
        List_node* next = create_node(value);
        curr_node->next = next;
    }
    list->length++;
}

void list_insert_before( List *list, int insert, int before ) {
  /* This function should take a pointer to a List *list,
   * a value to insert 'insert', and a value to insert before 'before'.
   * A new node should be inserted directly before the first
   * occurrence of "before" in the current list, like so:
   *
   * Starting with { 0 -> 5 -> 4 -> 5 }, call list_insert_before( list, -1, 5 ):
   * results in { 0 -> -1 -> 5 -> 4 -> 5 }
   *
   * NOTE: if the value 'before' does not exist in 'list', this
   * function should not modify the list or append anywhere.
   */
    List_node *curr_node = list->front;
    if (!curr_node) {
        return;
    } else if (curr_node->value == before) {
        List_node *new_node = create_node(insert);
        new_node->next = curr_node;
        list->front = new_node;
        list->length++;
    } else {
        while( curr_node->next != NULL ) {
            List_node *next_node = curr_node->next;
            if (next_node->value == before) {
                List_node *new_node = create_node(insert);
                curr_node->next = new_node;
                new_node->next = next_node;
                list->length++;
                break;
            } else {
                curr_node = curr_node->next;
            }
        }
    }
}

void list_delete( List *list, int value ) {
  /* Delete all occurrences of the value 'value' in list.
   * For example, starting with { 0 -> 5 -> 4 -> 5 }
   * call list_delete( list, 5 ):
   * results in { 0 -> 4 }
   * If there are no values to delete, the function should
   * do nothing.
   */
    List_node *curr_node = list->front;
    if (!curr_node) {
        return;
    }
    while (curr_node->value == value) {
        if (!curr_node->next) {
            list->front = NULL;
            list->length--;
            return;
        } else {
            curr_node = curr_node->next;
            list->front = curr_node;
            list->length--;
        }
    }
    while (curr_node->next != NULL) {
        List_node *next_node = curr_node->next;
        if (next_node->value == value) {
            curr_node->next = next_node->next;
            list->length--;
        }
        if (!curr_node->next) {
            // TODO: add list->back adjustment here
            break;
        }
        curr_node = curr_node->next;
    }
}

void list_apply( List *list, int (*function_ptr)(int) ) {
  /* Applies the function pointed to by function_ptr
   * to every value at nodes in list 'list'.
   * For example, starting with { 1 -> 2 -> 3 } and
   * a function 
   *
   *     int sq(int x) { return x * x; }
   * 
   * call to list_apply( list, sq );
   * results in { 1 -> 4 -> 9 }
   */
    List_node *curr_node = list->front;
    while (curr_node != NULL) {
        curr_node->value = function_ptr(curr_node->value);
        curr_node = curr_node->next;
    }
}

int list_reduce( List *list, int (*function_ptr)(int, int) ) {
  /* Takes an associative function pointed to by function_ptr
   * and returns the result of reducing the list with it.
   * For example, starting with { 1 -> 2 -> 3 } and
   * a function
   *
   *    int plus( int x, int y ) { return x + y; }
   * 
   * list_reduce( list, plus );
   * will return 1 + 2 + 3 = 6.
   * If the provided list contains 0 elements,
   * you should return 0; if the list has only one
   * element, return the value of that element.
   */
    int result;
    List_node *curr_node = list->front;
    if (!curr_node) {
        return 0;
    } else if (!curr_node->next) {
        return curr_node->value;
    } else {
        // Need initial value for result
        result = function_ptr(curr_node->value, curr_node->next->value);
        curr_node = curr_node->next;
        while (curr_node->next != NULL) {
            result = function_ptr(result, curr_node->next->value);
            curr_node = curr_node->next;
        }
    }
    return result;
}

// Print out a linked list in human-readable form
void list_print( List list ) {
  if( list.front == NULL ) {
    printf( "{}\n" );
  } else {
    printf( "{ " );

    List_node *p = list.front;
    size_t length = list.length;

    while( p->next != NULL && length > 0 ) {
      printf( "%d -> ", p->value );
      p = p->next; --length;
    }
    printf( "%d }\n", p->value );

    if( length != 1 ) {
      printf( "Error: badly formed list.\n" );
      exit( EXIT_FAILURE );
    }
  }
}

// Frees the memory in List *list
void list_clear( List *list ) {
  List_node *front = list->front;
  size_t length = list->length;

  while( front != NULL && length > 0 ) {
    List_node *next = front->next;
    free( front );
    front = next;
    --length;
  }

  if( length != 0 ) {
    printf( "Error: failed to clean up list properly.\n" );
    exit( EXIT_FAILURE );
  }
}
