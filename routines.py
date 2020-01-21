class Routine:
    delta_time = 0
    routines = []
    
    #? Well, idk if it is right, and probably it's not, but it works just fine so...
    #wait_for_seconds use class delta_time so it could be imported to all classes without passing references everywhere...

    def start_coroutine(routine):
        Routine.routines.append(routine)
        return routine

    def wait_for_seconds(time):
        timer = 0
        while timer < time:
            yield True
            timer += Routine.delta_time
