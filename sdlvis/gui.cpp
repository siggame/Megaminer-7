#include "gui.h"
#include "resources.h"

#include <iostream>
#include <cstdlib>
#include <string>
#include <sstream>

#include <SDL_ttf.h>

#define TOTAL_GOLD 0
#define OWNER 1
#define NUM_PIRATES 2
#define PIRATE_AVG_HEALTH 3
#define NUM_SHIPS 4
#define SHIP_AVG_HEALTH 5
#define TILE_X 6
#define TILE_Y 7
#define UNIT_INFO 8

using namespace std;

static SDL_Surface* screen = NULL;
static TTF_Font* font = NULL;
static TTF_Font* consoleFont = NULL;

bool arenaMode = false;

bool initGUI(bool arenaM)
{
  if( SDL_Init(SDL_INIT_VIDEO) <0 )
    return false;
  
  arenaMode = arenaM;
  
  if(!arenaMode)
  {
    screen = SDL_SetVideoMode(1024, 768, 32, SDL_HWSURFACE|SDL_DOUBLEBUF);
  }
  else
  {
    screen = SDL_SetVideoMode(1024, 768, 32, SDL_FULLSCREEN|SDL_DOUBLEBUF);
  }
  
  if(screen == NULL)
    return false;
  
  if( TTF_Init() < 0)
    return false;
  
  font=TTF_OpenFont("arial.ttf", 8);
  if(font == NULL)
    return false;
  
  consoleFont=TTF_OpenFont("arial.ttf", 20);
  if(consoleFont == NULL)
    return false;
}

void clearScreen()
{
  SDL_Rect dest;
  dest.x = dest.y = 0;
  dest.w = 1024;
  dest.h = 768;
  SDL_FillRect(screen, &dest, SDL_MapRGB(screen->format, 255, 255, 255));
}

void renderMap(Game& g)
{
  SDL_Surface* land = loadImage("images/land.png");
  SDL_Surface* water = loadImage("images/water.png");
  SDL_Surface* deepWater = loadImage("images/deep_water.png");
  SDL_Surface* sand = loadImage("images/sand.png");
    
  SDL_Rect dest;
  
  dest.w = 19;
  dest.h = 19;
  
  int tileTypes[40][40];
  
  for(int i = 0; i < g.states[0].tiles.size(); i++)
  {
    if(g.states[0].tiles[i].id == 0) continue;
    /*dest.x = g.states[0].tiles[i].x * 19;
    dest.y = g.states[0].tiles[i].y * 19;
      
    if(g.states[0].tiles[i].type)
    {
      bool isDeepWater = true;
      //it is water
      if(g.states[0].tiles[i].x > 0)
      {
        if(g.states[0].tiles[i].x - 1)
      
      SDL_BlitSurface(water, NULL, screen, &dest);
    }
    else
    {
      SDL_BlitSurface(land, NULL, screen, &dest);
    }*/
    
    tileTypes[g.states[0].tiles[i].x][g.states[0].tiles[i].y] = g.states[0].tiles[i].type;
  }
  
  for(int x = 0; x < 40; x++)
  {
    for(int y = 0; y < 40; y++)
    {
      dest.x = x * 19;
      dest.y = y * 19;
      
      /*if(x == 0 || x == 39 || y == 0 || y == 39)
      {
        if(tileTypes[x][y])
        {
          SDL_BlitSurface(water, NULL, screen, &dest);
        }
        else
        {
          SDL_BlitSurface(sand, NULL, screen, &dest);
        }
        
        continue;
      }*/
      
      bool superTile = true;
      
      if(x != 0)
      {
        if(!(tileTypes[x - 1][y] == tileTypes[x][y]))
        {
          superTile = false;
        }
      }
      
      if(superTile && x != 39)
      {
        if(!(tileTypes[x + 1][y] == tileTypes[x][y]))
        {
          superTile = false;
        }
      }
      
      if(superTile && y != 0)
      {
        if(!(tileTypes[x][y - 1] == tileTypes[x][y]))
        {
          superTile = false;
        }
      }
      
      if(superTile && y != 39)
      {
        if(!(tileTypes[x][y + 1] == tileTypes[x][y]))
        {
          superTile = false;
        }
      }
      
      /*if( tileTypes[x - 1][y] == tileTypes[x][y] &&
          tileTypes[x + 1][y] == tileTypes[x][y] &&
          tileTypes[x][y - 1] == tileTypes[x][y] &&
          tileTypes[x][y + 1] == tileTypes[x][y])*/
      if(superTile)
      {
        if(tileTypes[x][y])
        {
          SDL_BlitSurface(deepWater, NULL, screen, &dest);
        }
        else
        {
          SDL_BlitSurface(land, NULL, screen, &dest);
        }
      }
      else
      {
        if(tileTypes[x][y])
        {
          SDL_BlitSurface(water, NULL, screen, &dest);
        }
        else
        {
          SDL_BlitSurface(sand, NULL, screen, &dest);
        }
      }
    }
  }
}

void drawText(Game& g, int turn, int numships[2], int numpirates[2], int unitData[UNIT_INFO])
{
  stringstream message;
  SDL_Rect dest;
  dest.x = 768;
  dest.y = 2;
  SDL_Surface* image;
  SDL_Color purple = {255,0,255};
  SDL_Color red = {255,0,0};
  SDL_Color black = {0,0,0};
  SDL_Color blue = {0,0,255};
  SDL_Color yellow = {255,196,0};
  SDL_Color teamColor[2] = {{255,0,0},{0,0,255}};
  SDL_Color darkSlateGray = {47,79,79};
  
  message << "Current Turn: ";
  message << turn;
  
  image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
  SDL_BlitSurface(image, NULL, screen, &dest);
  dest.y += image->h;
  SDL_FreeSurface(image);
  dest.y += image->h;
  
  message.str("");
  
  for(int i = 0; i < 2; i++)
  {
    if(strcmp(g.states[turn].players[i].playerName,"booty()") == 0)
    {
      message << "booty(" << i + 1 << ")";
    }
    else
    {
      message << g.states[turn].players[i].playerName;
      message << " (" << i + 1 << ")";
    }
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), teamColor[i]);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "  Gold: ";
    message << g.states[turn].players[i].gold;
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), teamColor[i]);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "  Ships: ";
    message << numships[i];
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), teamColor[i]);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "  Pirates: ";
    message << numpirates[i];
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), teamColor[i]);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    dest.y += image->h;
  }
  
  if(turn >= g.states.size() - 1)
  {
    message << "Winner: ";
    
    if(strcmp(g.states[turn].players[g.winner].playerName,"booty()") == 0)
    {
      message << "booty(" << g.winner + 1 << "): ";
    }
    else
    {
      message << g.states[turn].players[g.winner].playerName;
      message << " (" << g.winner + 1 << "): ";
    }
    
    if(g.winner == 0)
    {
      image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), red);
    }
    else if(g.winner == 1)
    {
      image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), blue);
    }
    else
    {
      image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), black);
    }
    
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << g.winReason;
  
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), black);
    SDL_BlitSurface(image, NULL, screen, &dest);
    SDL_FreeSurface(image);
    dest.y += image->h*2;
    
    message.str("");
  }
  else
  {
    dest.y += image->h*3;
  }
  
  if(unitData[0] == -2)
  {
    dest.y += image->h*9;
  }
  else
  {
    message << "Info for (" << unitData[TILE_X] << "," << unitData[TILE_Y] << "):";
  
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), black);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    for(int i = 0; i < UNIT_INFO; i++)
    {
      switch(i)
      {
        case TOTAL_GOLD:
        {
          message << "Total Gold: " << unitData[i];
          break;
        }
        case OWNER:
        {
          if(unitData[i] <= -1)
          {
            message << "Owner: None";
          }
          else if(unitData[i] == 2 || unitData[i] == 3)
          {
            message << "Owner: Merchant";
          }
          else
          {
            message << "Owner: ";
            
            if(strcmp(g.states[turn].players[unitData[i]].playerName,"booty()") == 0)
            {
              message << "booty(" << unitData[i] + 1 << "): ";
            }
            else
            {
              message << g.states[turn].players[unitData[i]].playerName;
              message << " (" << unitData[i] + 1 << "): ";
            }
          }
          break;
        }
        case NUM_PIRATES:
        {
          message << "Pirates: ";
          image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
          SDL_BlitSurface(image, NULL, screen, &dest);
          dest.y += image->h;
          SDL_FreeSurface(image);
          message.str("");
          
          if(unitData[i] == 0)
          {
            message << "  Number: None";
          }
          else
          {
            message << "  Number: " << unitData[i];
          }
          break;
        }
        case PIRATE_AVG_HEALTH:
        {
          if(unitData[NUM_PIRATES] == 0)
          {
            message << "  Avg Health: None";
          }
          else
          {
            message << "  Avg Health: " << ((float)unitData[i]/(float)unitData[NUM_PIRATES]);
          }
          break;
        }
        case NUM_SHIPS:
        {
          message << "Ships: ";
          image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
          SDL_BlitSurface(image, NULL, screen, &dest);
          dest.y += image->h;
          SDL_FreeSurface(image);
          message.str("");
          
          if(unitData[i] == 0)
          {
            message << "  Number: None";
          }
          else
          {
            message << "  Number: " << unitData[i];
          }
          break;
        }
        case SHIP_AVG_HEALTH:
        {
          if(unitData[i] == 0)
          {
            message << "  Avg Health: None";
          }
          else
          {
            message << "  Avg Health: " << unitData[i];
          }
          break;
        }
        case TILE_X:
        case TILE_Y:
        {
          continue;
          break;
        }
      }
      
      
      if(i == OWNER)
      {
        if(unitData[i] == 0)
        {
          image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), red);
        }
        else if(unitData[i] == 1)
        {
          image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), blue);
        }
        else if(unitData[i] == 2 || unitData[i] == 3)
        {
          image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), yellow);
        }
        else
        {
          image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
        }
      }
      else
      {
        image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
      }
      
      SDL_BlitSurface(image, NULL, screen, &dest);
      dest.y += image->h;
      SDL_FreeSurface(image);
      
      message.str("");
      
    }
  }
  
  
  if(!arenaMode)
  {
    dest.y += image->h;
    message << "Controls:";
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), black);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "Space Bar = Pause";
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "Left Arrow = Decrease Turn";
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "Right Arrow = Increase Turn";
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "Up Arrow = Go to last Turn";
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
    
    message << "Down Arrow = Go to first Turn";
    
    image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), darkSlateGray);
    SDL_BlitSurface(image, NULL, screen, &dest);
    dest.y += image->h;
    SDL_FreeSurface(image);
    
    message.str("");
  }
  else
  {
    dest.y += image->h*7;
  }
  
  message << "                     Version: 0.603";
  
  image = TTF_RenderText_Solid(consoleFont, message.str().c_str(), purple);
  SDL_BlitSurface(image, NULL, screen, &dest);
  dest.y += image->h;
  SDL_FreeSurface(image);
}

void renderTurn(Game& g, int turn, int xTile, int yTile)
{
  
  SDL_Surface* ship_red = loadImage("images/ship_red.png");
  SDL_Surface* ship_blue = loadImage("images/ship_blue.png");
  SDL_Surface* ship_yellow = loadImage("images/ship_yellow.png");
  SDL_Surface* ship_none = loadImage("images/ship_none.png");
  SDL_Surface* pirate_red = loadImage("images/pirate_red.png");
  SDL_Surface* pirate_blue = loadImage("images/pirate_blue.png");
  SDL_Surface* pirate_yellow = loadImage("images/pirate_yellow.png");
  SDL_Surface* treasure = loadImage("images/treasure.png");
  SDL_Surface* selector = loadImage("images/selector.png");
  SDL_Surface* image = NULL;
  SDL_Rect dest;
  //SDL_Color yellow = {255,255,0};
  SDL_Color yellow = {0,255,0};
  //SDL_Color purple = {255,0,255};
  SDL_Color purple = {0,255,0};
  //SDL_Color black = {0,0,0};
  SDL_Color black = {0,255,0};
  SDL_Color color;
  char buf[9];
  dest.w = 19;
  dest.h = 19;
  int owner[40][40];
  int gold[40][40];
  int pirates[40][40];
  int ships[40][40];
  int piratesHealth[40][40];
  int shipsHealth[40][40];
  
  int unitData[UNIT_INFO];
  
  for(int i = 0; i < UNIT_INFO; i++)
  {
    unitData[i] = -2;
  }
  
  int numships[2] = {0,0};
  int numpirates[2] = {0,0};
  
  for(int i = 0; i < 40; i++)
  {
    for(int j = 0; j < 40; j++)
    {
      owner[i][j] = -1;
      gold[i][j] = 0;
      pirates[i][j] = 0;
      ships[i][j] = 0;
      shipsHealth[i][j] = 0;
      piratesHealth[i][j] = 0;
    }
  }
  
  clearScreen();
  renderMap(g);
  
  for(int i = 0; i < g.states[turn].ports.size(); i++)
  {
    if(g.states[turn].ports[i].id == 0) continue;
    if(g.states[turn].ports[i].owner == 0)
    {
      image = loadImage("images/port1.png");
    }
    else if(g.states[turn].ports[i].owner == 1)
    {
      image = loadImage("images/port2.png");
    }
    else
    {
      image = loadImage("images/port3.png");
    }
    dest.x = g.states[turn].ports[i].x * 19;
    dest.y = g.states[turn].ports[i].y * 19;
    SDL_BlitSurface(image, NULL, screen, &dest);
  }
  
  for(int i = 0; i < g.states[turn].treasures.size(); i++)
  {
    if(g.states[turn].treasures[i].id == 0) continue;
    gold[g.states[turn].treasures[i].x][g.states[turn].treasures[i].y] += g.states[turn].treasures[i].gold;
  }
  
  for(int i = 0; i < g.states[turn].pirates.size(); i++)
  {
    if(g.states[turn].pirates[i].id == 0) continue;
    pirates[g.states[turn].pirates[i].x][g.states[turn].pirates[i].y] += 1;
    gold[g.states[turn].pirates[i].x][g.states[turn].pirates[i].y] += g.states[turn].pirates[i].gold;
    owner[g.states[turn].pirates[i].x][g.states[turn].pirates[i].y] = g.states[turn].pirates[i].owner;
    piratesHealth[g.states[turn].pirates[i].x][g.states[turn].pirates[i].y] += g.states[turn].pirates[i].health;
  }
  
  for(int i = 0; i < g.states[turn].ships.size(); i++)
  {
    if(g.states[turn].ships[i].id == 0) continue;
    gold[g.states[turn].ships[i].x][g.states[turn].ships[i].y] += g.states[turn].ships[i].gold;
    ships[g.states[turn].ships[i].x][g.states[turn].ships[i].y] += 1;
    //dest.x = g.states[turn].ships[i].x * 19;
    //dest.y = g.states[turn].ships[i].y * 19;
    shipsHealth[g.states[turn].ships[i].x][g.states[turn].ships[i].y] += g.states[turn].ships[i].health;
    //SDL_BlitSurface(ship, NULL, screen, &dest);
  }
  
  for(int x = 0; x < 40; x++)
  {
    for(int y = 0; y < 40; y++)
    {
      if(ships[x][y] > 0)
      {
        dest.x = x * 19;
        dest.y = y * 19;
        
        if(owner[x][y] == 0)
        {
          SDL_BlitSurface(ship_red, NULL, screen, &dest);
          numships[0]++;
          numpirates[0] += pirates[x][y];
        }
        else if(owner[x][y] == 1)
        {
          SDL_BlitSurface(ship_blue, NULL, screen, &dest);
          numships[1]++;
          numpirates[1] += pirates[x][y];
        }
        else if(owner[x][y] == 2 || owner[x][y] == 3)
        {
          SDL_BlitSurface(ship_yellow, NULL, screen, &dest);
        }
        else
        {
          SDL_BlitSurface(ship_none, NULL, screen, &dest);
        }
      }
      else if(pirates[x][y] > 0)
      {
        dest.x = x * 19;
        dest.y = y * 19;
        
        if(owner[x][y] == 0)
        {
          SDL_BlitSurface(pirate_red, NULL, screen, &dest);
          numpirates[0] += pirates[x][y];
        }
        else if(owner[x][y] == 1)
        {
          SDL_BlitSurface(pirate_blue, NULL, screen, &dest);
          numpirates[1] += pirates[x][y];
        }
        else
        {
          SDL_BlitSurface(pirate_yellow, NULL, screen, &dest);
        }
      }
      else if(gold[x][y] > 0)
      {
        dest.x = x * 19;
        dest.y = y * 19;
        SDL_BlitSurface(treasure, NULL, screen, &dest);
      }
    }
  }
  
  for(int i = 0; i < 40; i++)
  {
    for(int j = 0; j < 40; j++)
    {
      if(gold[i][j] != 0)
      {
        dest.x = i * 19 + 10;
        dest.y = j * 19 + 19;
        
        sprintf(buf, "%d", gold[i][j]);
        image = TTF_RenderText_Solid(font, buf, yellow);
        dest.y -= image->h;
        dest.x -= image->w / 2;
        SDL_BlitSurface(image, NULL, screen, &dest);
        SDL_FreeSurface(image);
      }
      if(pirates[i][j] != 0)
      {
        dest.x = i * 19 + 10;
        dest.y = j * 19;
        
        if(owner[i][j] == 0)
        {
          color = black;
        }
        else if(owner[i][j] == 1)
        {
          color = purple;
        }
        else
        {
          color = yellow;
        }
          
        sprintf(buf, "%d", pirates[i][j]);
        
        image = TTF_RenderText_Solid(font, buf, color);
        dest.x -= image->w / 2;
        SDL_BlitSurface(image, NULL, screen, &dest);
        SDL_FreeSurface(image);
      }
    }
  }
  
  //now we draw the selector!
  if(xTile != -1 && yTile != -1)
  {
    dest.x = xTile * 19;
    dest.y = yTile * 19;
    
    SDL_BlitSurface(selector, NULL, screen, &dest);
    
    unitData[TOTAL_GOLD] = gold[xTile][yTile];
    unitData[OWNER] = owner[xTile][yTile];
    unitData[NUM_PIRATES] = pirates[xTile][yTile];
    unitData[PIRATE_AVG_HEALTH] = piratesHealth[xTile][yTile];
    unitData[NUM_SHIPS] = ships[xTile][yTile];
    unitData[SHIP_AVG_HEALTH] = shipsHealth[xTile][yTile];
    unitData[TILE_X] = xTile;
    unitData[TILE_Y] = yTile;
    
  }
  
  drawText(g, turn, numships, numpirates, unitData);
  
  //now draw the time thingy
  SDL_Rect timeBarDest;
  timeBarDest.x = 0;
  timeBarDest.y = 760;
  
  if(g.states.size() != 0)
  {
    timeBarDest.w = (int)((float)760 * (float)turn/(float)g.states.size());
  }
  else
  {
    timeBarDest.w = 760;
  }
  
  timeBarDest.h = 8;
  SDL_FillRect(screen, &timeBarDest, SDL_MapRGB(screen->format, 255, 0, 0));
  
  SDL_Flip(screen);
}

void mainLoop(Game& g, bool arenaMode)
{
  int turn = 0;
  
  bool render = true;
  bool killMe = false;
  
  while(true)
  {
    if(render)
    {
      renderTurn(g, turn, -1, -1);
    
      turn++;
    }
    
    if (turn >= g.states.size())
    {
      if(arenaMode)
      {
        long int counter = 0;
        while(counter != 2700000000)
        {
          counter++;
        }
        return;
      }
      render = false;
      killMe = false;
    }
    
    SDL_Delay(100);
    
    SDL_Event event;
    while ( SDL_PollEvent(&event) )
    {
      switch (event.type)
      {
        case SDL_QUIT:
        {
          return;
        }
        case SDL_MOUSEBUTTONDOWN:
        {
        //printf("Mouse button %d pressed at (%d,%d)\n",
        //      event.button.button, event.button.x, event.button.y);
        /*if(event.button.x > 500)
        {
          turn++;
          renderTurn(g, turn,-1, -1);
          render = false;
        }
        else
        {*/
          //render = !render;
        //}
          render = false;
          handleMouse(turn, event.button.x, event.button.y, g);
          break;
        }
        case SDL_KEYDOWN:
        {
          switch(event.key.keysym.sym)
          {
            case SDLK_ESCAPE:
            {
              return;
            }
            case SDLK_LEFT:
            {
              if(!render)
              {
                if(turn > 0)
                {
                  turn--;
                  renderTurn(g, turn, -1, -1);
                }
              }
              break;
            }
            case SDLK_RIGHT:
            {
              if(!render)
              {
                turn++;
                
                if (!(turn >= g.states.size()))
                {
                   renderTurn(g, turn, -1, -1);
                }
                else
                {
                  killMe = true;
                }
              }
              break;
            }
            case SDLK_UP:
            {
              render = false;
              turn = g.states.size() - 1;
              renderTurn(g, turn, -1, -1);
              break;
            }   
            case SDLK_DOWN:
            {
              render = false;
              turn = 0;
              renderTurn(g, turn, -1, -1);
              break;
            }         
            case SDLK_SPACE:
            {
              render = !render;
              break;
            }
          }
          break;
        }
      }
    }
    
    if(killMe)
    {
      return;
      break;
    }
  }
}

void handleMouse(int & turn, int x, int y, Game & g)
{
  int xTile = x/19;
  int yTile = y/19;
  
  if(yTile == 40 && xTile < 40)
  {
    turn = ((float)x/(float)760)*(float)g.states.size();
    renderTurn(g, turn, -1, -1);
  }
  
  if(xTile >= 40 || yTile >= 40)
  {
    return;
  }
  
  renderTurn(g, turn, xTile, yTile);
}
