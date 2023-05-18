#include <stdio.h>
#include <stdlib.h>

typedef struct LinkNode
{
    int val;
    struct LinkNode * next;
}LinkNode;


int main(){
    LinkNode * a = (LinkNode*)malloc(sizeof(LinkNode));
    a->val = 23333;
    a->next = NULL;
    printf("%d \n", sizeof(LinkNode));
    printf("%d \n", a -> val);

}