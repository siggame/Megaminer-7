//This file is for any functions you want to write that aren't directly part of your AI
//This file is shared, meaning the Java and Python clients can access it too if you want C++ code for whatever reason
#include "util.h"
#include "game.h"

#include <vector>
#include <deque>

#include <iostream>



//pathfinding code!

//all locations are integers
//y * width + x


static std::deque<int> path;

int getPathSize()
{
  return path.size();
}

int getPathStep(int i)
{
  return path[i];
}

int findPath(_Tile* start, _Tile* end, int type)
{
  //find the path between two tiles with breadth first search

  static int* grid = NULL; //grid indicating how each tile is reached
  int size = start->_c->mapSize;  
  std::deque<int> open;
  int startTile = start->y * size + start->x;
  int endTile = end->y * size + end->x;
  int tile;

  //empty the stored path
  path.clear();

  if(!grid)
  {
    grid = new int[size*size];
  }

  for(int i = 0; i < size; i++)
  {
    for(int j = 0; j < size; j++)
    {
      grid[i*size+j] = -1;
    }
  }

  grid[startTile] = -2; //Don't backtrack!
  open.push_back(startTile);



  while(open.size())
  {
    tile = open.front();
    open.pop_front();

    //std::cout << tile << std::endl;

    if(tile == endTile)
    {
      while(tile != startTile)
      {
        path.push_front(tile);
        tile = grid[tile];
      }
      return 1; //success
    }

    //can't path from land to sea or vice-versa
    if(start->_c->Tiles[tile].type != type && tile != startTile)
    {
      continue;
    }
    
    //left
    if(tile % size)
    {
      if(grid[tile-1] == -1)
      {
        open.push_back(tile-1);
        grid[tile-1] = tile;
      }
    }
    //up
    if((tile - size ) >= 0)
    {
      if(grid[tile-size] == -1)
      {
        open.push_back(tile-size);
        grid[tile-size] = tile;
      }
    }

    //right
    if((tile+1) % size)
    {
      if(grid[tile+1] == -1)
      {
        open.push_back(tile+1);
        grid[tile+1] = tile;
      }
    }
    //down
    if((tile + size ) < size*size)
    {
      if(grid[tile+size] == -1)
      {
        open.push_back(tile+size);
        grid[tile+size] = tile;
      }
    }
  }
  return 0; //failure
}

