import code

from basescript import BaseScript
import numpy as np

from .diskarray import DiskArray

class DiskArrayCommand(BaseScript):
    DESC = 'DiskArray command-line tool'

    DEFAULT_CAPACITY = None
    DEFAULT_GROWBY = 10000
    DEFAULT_MODE = 'r+'

    def interact(self):
        if self.args.capacity:
            capacity = eval(self.args.capacity)
        else:
            capacity = self.args.capacity

        fpath = self.args.fpath
        shape = eval(self.args.shape)
        growby = self.args.growby
        dtype = eval(self.args.dtype)
        mode = self.args.mode

        interact = DiskArray(fpath=fpath,
                shape=shape,
                capacity=capacity,
                growby=growby,
                dtype=dtype,
                mode=mode)

        namespace=dict(da=interact)
        code.interact("DiskArray Console", local=namespace)

    def define_subcommands(self, subcommands):
        super(DiskArrayCommand, self).define_subcommands(subcommands)

        interact_cmd = subcommands.add_parser('interact',
                help='DiskArray Console')
        interact_cmd.set_defaults(func=self.interact)
        interact_cmd.add_argument('fpath',
                help='Input file which is used to store disk arrys.\
                        eg: /tmp/disk.array')
        interact_cmd.add_argument('shape',
                help='shape is the size of the disk array.\
                        eg: \'(0, 3)\'')
        interact_cmd.add_argument('dtype',
                help='data type of the disk array.\
                        eg: np.float32')
        interact_cmd.add_argument('-c', '--capacity',
                default=self.DEFAULT_CAPACITY, type=str,
                help='capacity is the total capacity of the disk array.\
                        This is optional and default is shape value\
                        eg: --capacity \'(10, 3)\'')
        interact_cmd.add_argument('-g', '--growby',
                default=self.DEFAULT_GROWBY, type=int,
                help='growby is used to increase the size of\
                the disk array when it reaches to it\'s maximum limit.\
                This is optional and default is 10000\
                eg: --growby 200')
        interact_cmd.add_argument('-m', '--mode',
                default=self.DEFAULT_MODE, type=str,
                help='mode is to open the disk array in that mode.\
                        Example modes are r+, r, w+ and c\
                        This is optional and default is r+')

def main():
    DiskArrayCommand().start()

if __name__ == '__main__':
    main()
