#!/usr/bin/env python

import ncs.maapi
import ncs.maagic

def allocate_id():
    with ncs.maapi.single_write_trans('admin', 'system') as t:
        root = ncs.maagic.get_root(t)
        db = root.l2vpn__id_database
        try:
            l = db.used_ids
            if l is None: l = list()
            allocated_id = [n for n in range(db.start, db.stop) if n not in l][0]
            l.append(allocated_id)
            db.used_ids = l
            t.apply()
            return allocated_id
        except IndexError:
            raise Exception('Exhausted all IDs!')

def deallocate_id(i):
    with ncs.maapi.single_write_trans('admin', 'system') as t:
        root = ncs.maagic.get_root(t)
        db = root.l2vpn__id_database
        l = db.used_ids
        if l is None: return
        try:
            l.remove(i)
            db.used_ids = l
            t.apply()
        except ValueError:
            pass


def main():
    print 'Testing Fake External Allocator'
    allocated_id = allocate_id()
    print 'Allocated ID:', allocated_id

    deallocate_id(allocated_id)
    print 'Successfully deallocated ID!'

if __name__ == '__main__':
    main()