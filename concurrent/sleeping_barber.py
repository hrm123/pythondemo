import threading
import time
import random
from enum import Enum

# Note - threading.Lock() is thread level mutex (saves when compound statements need to run atomically safe against thread switching).
# Although Python features a Global Interpreter Lock (GIL) that prevents multiple threads from executing Python bytecodes simultaneously, 
# you still need mutex locks for thread-safe code because Python can switch threads in the middle of non-atomic operations ( like a += 10)
# For mutex where multi-processing is needed, use multiprocessing.Lock() instead of threading.Lock().
# ~~ Lock for synchronizing access to piece of code block ~~ A lock (threading.Lock() etc.) ensures that only one thread can execute a specific block of code at any given time. 
# If a second thread tries to enter that code block while the first thread is inside, the second thread must wait until the lock is released.
# ~~ Lock for syncrhonizing access to shared resources (variable/field etc.) ~~ Locks are often used to protect shared resources (like variables, data structures, or files) 
# from being accessed by multiple threads simultaneously. A lock does not magically 
# attach itself to a variable or field to stop other code from reading or writing
# it. If you modify a field inside a locked code section, that field is protected 
# only if every other thread also uses that exact same lock when accessing or modifying
# that field. If another piece of code modifies the field without acquiring the lock,
# a race condition can still happen. It might be better to keep fields private and have setter and getter methods which use the same 'lock'
# so that the shared field/resource is protected against multiple thread access.

# Python does not have concept of private fields or functions. It is naming convention
# that will indicate if a field/function is private  or not. Usually an _ added before field name or function name means they are supposed to be private to the class
# declaring them. But they are still accessible from outside the class. Python does not have concept of protected fields or functions.



class BarberState(Enum):
    RUNNING = 0,
    STOPPED = 1,
    CUTTING = 2,
    SLEEPING = 3,
    AWAKE = 4

class CustomerState(Enum):
    SEATED = 0,
    GETTING_HAIR_CUT = 1,
    EXITED = 2,
    HAIRCUT_DONE=3,
    ENTERING = 4

class SaloonState(Enum):
    FULL = 0,
    EMPTY = 1,
    PARTIALLY_FULL = 2

'''
    Chair Uses  'lock' to give access to only one customer at a time to occupy a chair.
'''
class Chair:
    def __init__(self, chair_id):
        self.chair_id = chair_id
        self.isOccupied = False
        self.lock = threading.RLock()
        self.customer_id = None  # Track which customer is occupying the chair

    def occupy_chair(self, customer_id: str) -> bool:
        if self.lock.acquire(blocking=False):  # Try to acquire the lock without blocking (with lock blocks indefinitely and hence not used)        
            print(f"Customer {customer_id} could not occupy chair {self.chair_id} since clock getting a lock expired")
            self.lock.release()
            return False
        if self.isOccupied or not self.customer_id is None:
            print(f"Customer {customer_id} could not occupy chair {self.chair_id} as it is already occupied by {self.customer_id}")
            self.lock.release()
            return False        
        self.isOccupied = True
        self.customer_id = customer_id
        print(f"Customer {customer_id} occupied chair {self.chair_id}")
        return True

    def vacate_chair(self, customer_id: str) -> bool:
        if not self.isOccupied and self.customer_id is None:
            return True  # Chair is already vacant, nothing to do
        with self.lock:  # Ensure that the vacate operation is atomic.. it is okay to block on the lockign since we know it will be released after few operations
            if self.isOccupied and self.customer_id == customer_id:
                self.isOccupied = False
                self.customer_id = None
                print(f"Customer {customer_id} vacated chair {self.chair_id}")
                return True
            else:
                print(f"Customer {customer_id} could not vacate chair {self.chair_id} occupied by {self.customer_id}. Something wrong")
                return False

'''
    Saloon Uses  'lock' to give atomic access chairs to customer only if any chair is empty.
    Also uses the same 'lock' to ensure that barber/customer view of the saloon seating is consistent.
'''

class Saloon:
    def __init__(self, num_chairs, num_customers):
        self.__num_chairs = num_chairs
        self.__waiting_customers = [Customer(i, self) for i in range(num_customers)]
        self.__state = SaloonState.EMPTY
        self.__lock = threading.RLock() # lock saloon to atomically update customer entry/exit/barber checking
        self.__chairs = [Chair(i) for i in range(num_chairs)]

    @property
    def SaloonState(self):
        return self.__state
   
    def get_chair_for_customer(self, customer_id: str) -> bool:
        if not self.__lock.acquire(blocking=True, timeout=1)  # Acquire the lock to ensure atomic access to chairs.. wait for 1 second to get the access
            print(f"problem acquiring lock to saloon and chair not assigned to customer")
            return False  # Could not acquire lock, return None
        occupied_chair = None
        for chair in self.__chairs:
            if not chair.isOccupied:
                if chair.occupy_chair(customer_id):
                    occupied_chair = chair
                    break
        if occupied_chair is None:
            print(f"problem acquiring chair to customer")
            self.__lock.release()
            return False
        if self.__num_chairs == len(self.__waiting_customers):
            self.__state = SaloonState.FULL
        else:
            self.__state = SaloonState.PARTIALLY_FULL
        self.__lock.release()
        return (True if occupied_chair is not None else False)  # Return the occupied chair or None if no available chairs

    '''
    Customer calls this when the customer wants to go out without haircut. 
    Saloon calls this (from send_next_customer_to_barber) when barber requests for next customer
    '''
    def release_customer_from_chair(self, chair: Chair, customer_id: str):
        if not self.__lock.acquire(blocking=True, timeout=1)  # Acquire the lock to ensure atomic access to chairs.. wait for 10 second to get the access
            print(f"Customer {customer_id} could not be released from chair {chair.chair_id} as the saloon lock could not be acquired. SOMETHING might be WRONG. Retry few times")
            return None  # Could not acquire lock, return None
        if chair.vacate_chair(customer_id):
            self.__waiting_customers.remove(customer_id)
            if len(self.__waiting_customers) > 0:
                self.state = SaloonState.PARTIALLY_FULL
            else:
                self.state = SaloonState.EMPTY
        else:
            print(f"Customer {customer_id} could not be released from chair {chair.chair_id} as it was not occupied by them")
        self.__lock.release()

    '''
    Saloon calls this when barber requests for next customer
    '''
    def send_next_customer_to_barber(self, customer_id: str) -> Customer|None: # only Barber can call this method
        self.__lock.acquire(blocking=True, timeout=1)  # Acquire the lock to ensure atomic access to chairs and barber
        if self.state == SaloonState.EMPTY:
            print(f"Customer {customer_id} found the saloon empty and left.")
            self.__lock.release()
            return None
        next_customer = self.__waiting_customers.pop(0)  # Remove the customer from the waiting list
        next_customer_chair = next((chair for chair in self.__chairs if chair.customer_id == next_customer), None)
        if next_customer_chair:
            next_customer_chair.vacate_chair(next_customer.customer_id)  # Release the chair occupied by the customer
        self.__lock.release()
        next_customer.set_customer_state = CustomerState.GETTING_HAIR_CUT
        return next_customer  # Return the next customer to be served by the barber

    def saloon_open(self):
        while

        
'''
    Is a thread (uses composition since it is referred to inheriting from Thread class).
    Occasionally checks if any customer is waiting. If yes, then cut hair. If no customer is there, then go to sleep    
'''
class Barber:
    def __init__(self, saloon, xname: str):
        self._thread = threading.Thread(target=self._start_working)
        self.name = xname
        self.is_running = False
        self.__saloon = saloon

    def _start_working(self):
        # look to see if any customer is there. If yes, then cut hair. If no customer is there, then go to sleep
        self.is_running = True
        while self.is_running is True: # Saloon will make 'is_running' False when it is closing time
            nextCustomer = self.__saloon.send_next_customer_to_barber()
            while nextCustomer is not None:
                self.state = BarberState.CUTTING
                self.cut_hair(nextCustomer)
                nextCustomer.customer_state = CustomerState.HAIRCUT_DONE
                nextCustomer = self.__saloon.send_next_customer_to_barber()
            self.go_to_sleep() # go to sleep if no customer is there
        return #ends the barber thread

    def go_to_sleep(self):
        self.state = BarberState.SLEEPING
        time.sleep(random.randint(1, 10))  # Simulate barber going to sleep
        self.state = BarberState.AWAKE

    def cut_hair(self, customer):
        print(f"Barber is cutting hair of Customer {customer.customer_id}")
        time.sleep(2)  # Simulate time taken to cut hair
        print(f"Barber finished cutting hair of Customer {customer.customer_id}")

'''
Is a thread (uses composition since it is referred to inheriting from Thread class).
Checks if any chair is empty in saloon (by asking Saloon). If yes, occupies that chair else exits.
Once occupies any chair then waits till Barber calls the customer to get haircut.
Once haircut is done, barber  calls exitSaloon method on Customer.
'''
class Customer:
    def __init__(self, customer_id, saloon):
        self.customer_id = customer_id
        self.saloon = saloon
        self.__thread = threading.Thread(target=self._enter_saloon)
        self.lock = threading.RLock()
        self.is_running = True
        self.__state = CustomerState.ENTERING
        self.__thread.start()

    @property
    def customer_state(self)-> CustomerState:
        return self.__state

    @customer_state.setter
    def set_customer_state(self, value) -> bool:
        self.__state = value
        return True

    def _enter_saloon(self):
        if self.saloon.get_chair_for_customer() is True:
            self.__state = CustomerState.SEATED
            print(f"Customer {self.customer_id} is seated.")
        else:
            print(f"Customer {self.customer_id} found no available chairs and left.")
        while self.is_running is True and self.__state is not CustomerState.HAIRCUT_DONE: # Saloon may make 'is_running' false when it is closing time
            time.sleep(random.randint(1, 10))
        print(f"Customer {self.customer_id} haircut is done.")
        time.sleep(random.randint(1, 10))
        self.__state = CustomerState.EXITED
        print(f"Customer {self.customer_id} exited.")
        return #ends the customer thread

    class OneCustomerTest:
    
        def __init__(self):
            self.saloon = Saloon(1, 1)

        def run_test(self):
            server_customers = self.cus
