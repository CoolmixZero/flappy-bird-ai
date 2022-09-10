from src import Base, Bird, Pipe
from settings import *


def draw_window(window, birds, pipes, base, score, gens_count):
    """
    draws the windows for the main game loop
    :param window: pygame window surface
    :param birds: a Bird object
    :param pipes: List of pipes
    :param base: Base object
    :param score: score of the game (int)
    :param gens_count: current generation
    :return: None
    """
    window.blit(BG_IMG, (0, 0))
    pygame.display.set_caption("Flappy Bird AI")
    pygame.display.set_icon(BIRD_IMAGES[2])

    for pipe in pipes:
        pipe.draw(window)

    score_label = STATS_FONT.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    score_label = STATS_FONT.render("Gens: " + str(gens_count - 1), True, (255, 255, 255))
    window.blit(score_label, (10, 10))

    score_label = STATS_FONT.render("Alive: " + str(len(birds)), True, (255, 255, 255))
    window.blit(score_label, (10, 50))

    base.draw(window)

    for bird in birds:
        bird.draw(window)

    pygame.display.update()


GENS_COUNT = 0


def fitness(genomes, config):
    nets = []
    ge = []
    birds = []

    global GENS_COUNT
    GENS_COUNT += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        base.move()

        add_pipe = False
        removed_pipes = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed_pipes.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for pipe in removed_pipes:
            pipes.remove(pipe)
        for x, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(window, birds, pipes, base, score, GENS_COUNT)
