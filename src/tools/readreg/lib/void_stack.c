/*
 * This is a really simple implementation of a stack which stores chunks
 * of memory of any type.  It still needs work to eliminate memory
 * leaks. 
 *
 * Copyright (C) 2005,2007 Timothy D. Morgan
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2 of the License.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.  
 *
 * $Id$
 */

#include "../include/void_stack.h"

void_stack* void_stack_new(unsigned short max_size)
{
  void_stack* ret_val = (void_stack*)malloc(sizeof(void_stack));

  if (ret_val != NULL)
  {
    memset(ret_val, 0, sizeof(*ret_val));
    ret_val->elements = (void**)malloc(max_size*sizeof(void*));
    if (ret_val->elements == NULL)
    {
      free(ret_val);
      ret_val = NULL;
    }
    else
    {
      memset(ret_val->elements, 0, max_size*sizeof(void*));
    
      ret_val->max_size = max_size;
      ret_val->top = 0;
    }
  }

  return ret_val;
}


void_stack* void_stack_copy(const void_stack* v)
{
  unsigned int i;
  void_stack* ret_val;
  if(v == NULL)
    return NULL;

  ret_val = void_stack_new(v->max_size);
  if(ret_val == NULL)
    return NULL;

  for(i = 0; i < v->top; i++)
    ret_val->elements[i] = v->elements[i];
  ret_val->top = v->top;

  return ret_val;
}


void_stack* void_stack_copy_reverse(const void_stack* v)
{
  unsigned int i;
  void_stack* ret_val;
  if(v == NULL)
    return NULL;

  ret_val = void_stack_new(v->max_size);
  if(ret_val == NULL)
    return NULL;

  for(i = 0; i < v->top; i++)
    ret_val->elements[i] = v->elements[v->top-i-1];
  ret_val->top = v->top;

  return ret_val;
}


void void_stack_free(void_stack* stack)
{
  free(stack->elements);
  free(stack);
}


void void_stack_free_deep(void_stack* stack)
{
  unsigned short i;
  for(i=0; i < stack->top; i++)
    free(stack->elements[i]);
  free(stack->elements);
  free(stack);
}


unsigned short void_stack_size(const void_stack* stack)
{
  return stack->top;
}


void* void_stack_pop(void_stack* stack)
{
  void* ret_val = NULL;

  if(stack->top > 0)
  {
    ret_val = stack->elements[--(stack->top)];
    stack->elements[stack->top] = NULL;
  }

  return ret_val;
}


bool void_stack_push(void_stack* stack, void* e)
{
  if(stack->top < stack->max_size)
  {
    stack->elements[stack->top++] = e;
    return true;
  }
  else
    return false;
}


const void* void_stack_cur(const void_stack* stack)
{
  void* ret_val = NULL;

  if(stack->top > 0)
    ret_val = stack->elements[stack->top-1];

  return ret_val;
}


void_stack_iterator* void_stack_iterator_new(const void_stack* stack)
{
  void_stack_iterator* ret_val = NULL;
  
  if(stack != NULL)
  {
    ret_val = (void_stack_iterator*)malloc(sizeof(void_stack_iterator));
    if (ret_val != NULL)
    {
      ret_val->stack = stack;
      ret_val->cur = 0;
    }
  }

  return ret_val;
}


void void_stack_iterator_free(void_stack_iterator* iter)
{
  free(iter);
}


const void* void_stack_iterator_next(void_stack_iterator* iter)
{
  if(iter->cur < iter->stack->top)
    return iter->stack->elements[iter->cur++];
  else
    return NULL;
}
