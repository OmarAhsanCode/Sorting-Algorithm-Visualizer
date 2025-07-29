import math
import pygame
import random #provides a random number generator
pygame.init() #initializes the pygame module

class DrawInformation:  #This class will be used to store the information needed to draw the game
    BLACK=(0,0,0)
    WHITE=(255,255,255)
    GREEN=(0,255,0)
    RED=(255,0,0)
    BLUE=(0,0,255)
    
    BACKGROUND_COLOR=PINK=METALLIC_SEAWEED=(0, 128, 128)

    GRADIENTS=[
        (255,223,0),
        (212,175,55),
        (153,101,21),
        
    ]

    FONT = pygame.font.SysFont('gravitas-one-regular', 35)
    LARGE_FONT = pygame.font.SysFont('gravitas-one-regular', 50)

    SIDE_PAD=100
    TOP_PAD=150

    def __init__(self,width,height,lst):  #Constructor
        self.width=width
        self.height=height

        self.window=pygame.display.set_mode((width,height)) #Set the window size
        pygame.display.set_caption("Sorting Algorithm Visualizations") #Set the window title
        self.set_list(lst) #Set the list to be drawn

    def set_list(self,lst):
        self.lst=lst 
        self.max=max(lst) #Find the maximum and minimum values in the list
        self.min=min(lst)    

        self.block_width=round((self.width-self.SIDE_PAD)/len(lst)) #Calculate the width of each bar
        self.block_height= math.floor((self.height-self.TOP_PAD)/(self.max-self.min)) #Calculate the height of each bar
        self.start_x=self.SIDE_PAD//2 #Calculate the starting x position of the first bar


def draw(draw_info, algo_name, ascending): #Draw the game
    draw_info.window.fill(draw_info.BACKGROUND_COLOR) #Fill the window with the background color

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.WHITE) #Create the title text
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5)) #Center the title text

    controls = draw_info.FONT.render("R - Reset | Space - Start Sorting | A - Ascending | D - Descending", 1, draw_info.WHITE) #Create the controls text
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 40)) # Center the controls text
    
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.WHITE) 
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 65)) 


    draw_list(draw_info) #Draw the list of numbers
    pygame.display.update() #Update the display

def draw_list(draw_info, color_positions={}, clear_bg=False): #Draw the list of numbers
    lst=draw_info.lst

    if clear_bg:
        clear_rect= (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width-draw_info.SIDE_PAD, draw_info.height-draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)



    for i, val in enumerate(lst):
        x = draw_info.start_x+i*draw_info.block_width  #Calculate the x position of the bar
        y = draw_info.height - (val-draw_info.min)*draw_info.block_height  #Calculate the y position of the bar

        color = draw_info.GRADIENTS[i%3] #Alternate between the three gradient colors

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width, draw_info.height)) #Draw the bar

    if clear_bg:
        pygame.display.update()    




def generate_starting_list(n, min_val, max_val): #Generates a list of n random numbers between min_val and max_val
    lst=[]
    
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending = True): #Bubble sort algorithm
    lst=draw_info.lst

    for i in range(len(lst)-1): #Loop through the list
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2=lst[j+1]

            if (num1>num2 and ascending) or (num1<num2 and not ascending): #If the numbers are in the wrong order, swap them
                lst[j],lst[j+1]=lst[j+1],lst[j]
                draw_list(draw_info, {j:draw_info.BLACK, j+1:draw_info.WHITE}, True)
                yield True #This will cause the generator to pause and return control to the main loop
    return lst  #Return the sorted list

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst



def main(): #Main function
    run = True
    clock = pygame.time.Clock() #This will be used to control the frame rate of the game

    n=50
    min_val=0
    max_val=100

    lst = generate_starting_list(n,min_val,max_val)
    draw_info=DrawInformation(800,600,lst)
    sorting=False
    ascending=True

    sorting_algorithm = bubble_sort
    sorting_algo_name="Bubble Sort"
    sorting_algorithm_generator=None

    while run:
        clock.tick(120) #This will make the game run at 60 frames per second

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting=False
        else:        
            draw(draw_info,sorting_algo_name,ascending)

        for event in pygame.event.get(): #This will check if the user has closed the window
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN: #Check if a key has been pressed
                continue

            if event.key == pygame.K_r: #If the 'r' key is pressed, generate a new list
                lst = generate_starting_list(n,min_val,max_val) 
                draw_info.set_list(lst)    
                sorting=False   
            elif event.key == pygame.K_SPACE and sorting == False: #If the space key is pressed, start sorting the list
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting: #If the 'a' key is pressed, sort the list in ascending order
                ascending = True
            elif event.key == pygame.K_d and not sorting: #If the 'd' key is pressed, sort the list in descending order
                ascending = False
            elif event.key == pygame.K_i and not sorting: 
                sorting_algorithm = insertion_sort
                sorting_algo_name="Insertion Sort"
            elif event.key == pygame.K_b and not sorting: 
                sorting_algorithm = bubble_sort
                sorting_algo_name="Bubble Sort"
    pygame.quit()   


if __name__ == "__main__": #This will run the main function if the script is run directly
    main()

    

