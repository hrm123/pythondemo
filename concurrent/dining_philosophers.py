
'''
Problem - 5 philosophers sitting in round table with 5  seats and 5 forks. 
Each philosopher needs 2 forks to eat. The philosophers can either be thinking 
or eating. A philosopher can only pick up the fork on their left and the fork 
on their right. If a philosopher cannot pick up both forks, they will put down
any fork they have picked up and go back to thinking (to avoid starvation). Eating
takes random time, after which the philosopher will put down both 
forks and leaves the dining room. After thinking for some random time,
philosopher again becomes hungry, and the circle repeats itself.

Facts derived -
Fork can be picked up by only one philosopher at a time. That too only either of 
the philosophers that sit adjacent to the fork.

Philosopher has 4 states - thinking, eating, picking up fork, putting down fork.
Picking/putting down a fork are atomic actions. Eating and thinking require random time.
can be done atomically, only one state at a time, and 


Solution - 2 approached might be possible (1) where philosopher polls for forks and (2) where philosopher waits for forks. We will implement the first approach.    

Since adjacency is important - Philosophers will have number as their ID and 
forks have number as their ID. We can go round the table starting with philosopher #1,
fork #1, philosopher #2, fork #2, and so on. The fork with ID i is to the left of
philosopher with ID i and to the right of philosopher with ID (i+1)%5.

If a philosopher cannot pick up both forks, they will put down
any fork they have picked up and go back to thinking (to avoid starvation & deadlock 
& livelock). They will only lock the first fork that is picked and just check if 
second fork is available. If not, they will put down the first fork and go back to thinking.


class Fork {
 int ID
 bool isAvailable = true

 LockFork(int philosopherID){
    // check if this philosopher can lock this fork (TODO later)
    // check if fork is available, if yes, lock it (interlocked change status of isAvailable)
    // and return true. If not, return false.

 }
 
 UnlockFork(int philosopherID){
    // check if this philosopher can unlock this fork (TODO later) 

    // check if fork is unavailable, if yes, make it available 
    // (interlocked change status of isAvailable)
    // and return true. If not, return false.
 }

}

class Philosopher Derives Thread {
    Fork left_fork, right_fork // assigned as properties
    int ID // assigned in constructor
    state = thinking | eating | picking_up_fork | putting_down_fork

    think(){
        // think for random time thread.sleep(random_time)
    }

    eat(){
        // eat for random time thread.sleep(random_time)
    }

    pick_up_forks(){
        // pick up left fork if it is available and then lock it.
        // pick up right fork if it is available and then lock it. If
        // not available, put down left fork and go back to thinking

        // if both forks are locked by philosopher, go to eating state and after
        // random time, put down both forks and leave the dining room (thread ends)
    }

    put_down_forks(){
        // put down left fork
        // put down right fork
        left_fork.unlock(this.ID);
        right_fork.unlock(this.ID);
        //exit the dining room (thread ends)
    }
}


'''
import threading
import time
import random
from enum import Enum
import typing

class Fork:
    
    def __init__(self, xID : int):
        self.ID = xID
        self.isAvailable = True
        self.lock = threading.Lock()

    def lock_fork(self, philosopher_id : str, wait_on_lock : bool = False, tout: int = 60) -> bool:      
        if wait_on_lock and self.lock.acquire(blocking=wait_on_lock, timeout=tout): # wait for the specified time to acquire a lock
            self.isAvailable = False
            print(f"Philosopher {philosopher_id} locked fork {self.ID}")
            return True
        elif not wait_on_lock and self.lock.acquire(blocking=wait_on_lock): # do not wait for the lock, just try to acquire it
            self.isAvailable = False
            print(f"Philosopher {philosopher_id} locked fork {self.ID}")
            return True
        else:
            print(f"Philosopher {philosopher_id} could not lock fork {self.ID} as it is already locked")
            return False

    def unlock_fork(self, philosopher_id : str) -> bool:
        if not self.isAvailable:
            self.lock.release()
            self.isAvailable = True
            print(f"Philosopher {philosopher_id} unlocked fork {self.ID}")
            return True
        else:
            print(f"Philosopher {philosopher_id} could not unlock fork {self.ID} as it is already unlocked")
            return False
    
    def __del__(self):
        if not self.isAvailable:
            self.lock.release()
            self.isAvailable = True
            print(f"Fork {self.ID} is being deleted and unlocked")

class PhilosopherState(Enum):
    CREATED = 0,
    THINKING = 1
    EATING = 2
    PICKING_UP_FORKS = 3
    PUTTING_DOWN_FORKS = 4
    EXIT_DINING = 5,
    ENTER_DINING = 6


class Philosopher():
    
    def __init__(self, xname : str, lf: Fork, rf: Fork):
        self._thread = threading.Thread(target=self._start_dining)
        self.name = xname
        self.l_f = lf
        self.r_f = rf
        self.st = PhilosopherState.CREATED
        print(f"{self.name} - {self.st.name}")
        self.ate = False
        self.max_running_time = 120 # seconds
        self.is_running = False

    def _think(self):
        self.st = PhilosopherState.THINKING
        print(f"{self.name} - {self.st.name}")
        time.sleep(random.randint(1, 10))

    def _eat(self):
        self.st = PhilosopherState.EATING
        print(f"{self.name} - {self.st.name}")
        time.sleep(random.randint(1, 10))
        self.ate = True

    def _pick_up_forks(self):
        self.st = PhilosopherState.PICKING_UP_FORKS
        print(f"{self.name} - {self.st.name}")
        # deadlock could happen when holding a resource and then waiting for anotehr resource.
        # we avoid that by blocking ly on the first fork and then checking if the 
        # second fork is available. If not, we put down the 
        # first fork and go back to thinking.
        print(f"{self.name} is trying to pick up left fork {self.l_f.ID}")
        if self.l_f.lock_fork(self.name, wait_on_lock=True):
            print(f"{self.name} is picked left fork {self.l_f.ID} and now trying to pick up right fork {self.r_f.ID}  ")
            if self.r_f.lock_fork(self.name):
                print(f"{self.name} has picked up both forks and is ready to eat")
                return True
            else:
                print(f"{self.name} could not pick up right fork and is putting down left fork")
                self.l_f.unlock_fork(self.name)
                self.l_f, self.r_f = self.r_f, self.l_f # swap forks to avoid starvation
                return False
        else:
            print(f"{self.name} could not pick up left fork and is going back to thinking")
            return False

    def _put_down_forks(self):
        self.st = PhilosopherState.PUTTING_DOWN_FORKS
        print(f"{self.name} - {self.st.name}")
        self.l_f.unlock_fork(self.name)
        self.r_f.unlock_fork(self.name)
        print(f"{self.name} has put down both forks")

    def _exit_dining(self):
        self.st = PhilosopherState.EXIT_DINING
        print(f"{self.name} - {self.st.name}")
        self._put_down_forks()
        self._is_running = False
        # self._thread.join()
        print(f"{self.name} has left the dining room")

    def enter_dining_room(self):
        self.st = PhilosopherState.ENTER_DINING
        print(f"{self.name} - {self.st.name}")
        self._thread.start()
        self.is_running = True


    def _start_dining(self):
        start_time = time.time()
        self.is_running = True
        while not self.ate and time.time() - start_time < self.max_running_time:
            if self._pick_up_forks():
                self._eat()
                self.ate=True
        if self.ate:
            self._exit_dining()

class DiningRoom:
    
    def __init__(self, num_of_philosophers: int = 5):
        self.forks = [Fork(i) for i in range(num_of_philosophers if num_of_philosophers > 1 else 2)]
        if num_of_philosophers != 1:
            self.philosophers = [Philosopher(f"Philosopher {i},{i+1 if (i!=num_of_philosophers-1) else 0}", self.forks[i], self.forks[i+1 if (i!=num_of_philosophers-1) else 0]) for i in range(num_of_philosophers)]
        else:
            self.philosophers = [Philosopher(f"Philosopher {0},{1}", self.forks[0], self.forks[1])]

    def start_dining(self):
        for philosopher in self.philosophers:
            philosopher.enter_dining_room()


class OneDiningPhilosophersTest:
    
    def __init__(self):
        self.dining_room = DiningRoom(1)

    def run_test(self):
        self.dining_room.start_dining()
        # since we are not craeting anydaemon threads, python interpreter will wait ti all the created threads have exited
        
class TwoDiningPhilosophersTest:
    
    def __init__(self):
        self.dining_room = DiningRoom(2)

    def run_test(self):
        self.dining_room.start_dining()
        # since we are not craeting anydaemon threads, python interpreter will wait ti all the created threads have exited


if __name__ == "__main__":
    test = TwoDiningPhilosophersTest()
    test.run_test()