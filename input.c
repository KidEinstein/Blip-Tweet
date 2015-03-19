#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/fcntl.h>
int main (int argc, char* argv[])
{
    while (1) {
        char* file = "output.txt";
        int fd;
        struct flock lock;
        printf ("opening %s\n", file);
        /* Open a file descriptor to the file. */
        fd = open ("output.txt", O_RDONLY);
        printf ("locking\n");
        /* Initialize the flock structure. */
        memset (&lock, 0, sizeof(lock));
        lock.l_type = F_RDLCK;
        /* Place a write lock on the file. */
        printf("Unlock : %d", fcntl (fd, F_SETLKW, &lock));

        printf ("locked; hit Enter to unlock... ");
        /* Wait for the user to hit Enter. */
        getchar ();

        printf ("unlocking\n");
        /* Release the lock. */
        lock.l_type = F_UNLCK;
        fcntl (fd, F_SETLKW, &lock);

        close (fd);
    }
    return 0;
}
