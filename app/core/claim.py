class Status:
    def __init__(self, name: str, value: int):
        self.name: str = name
        self.value: int = value

    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return self.name # String representation

class Claim:
    ok: Status = Status(name="ok", value=1)
    water: Status = Status(name="water", value=2)
    self_owned: Status = Status(name="self_owned", value=4)
    other_owned: Status = Status(name="other_owned", value=8)
    not_adjacent: Status = Status(name="not_adjacent", value=16)

    list: dict[str, Status] = {"not_adjacent": not_adjacent, # 16
                               "other_owned": other_owned,   # 8
                               "self_owned": self_owned,     # 4
                               "water": water,               # 2
                               "ok": ok}                     # 1
    
    max: int = sum(obj.value for _, obj in list.items())

    def is_valid(code: int) -> bool:       
        # Code out of range
        if (code > Claim.max):
            return False 
        if (code < 1):
            return False
        
        stats = Claim.check(code=code)

        # Owned by self and other
        case1 = [Claim.self_owned, Claim.other_owned]
        if all(s in stats for s in case1):
            return False
        
        # OK but owned by other
        case2 = [Claim.ok, Claim.other_owned]
        if all(s in stats for s in case2):
            return False

        # OK but owned by self
        case3 = [Claim.ok, Claim.self_owned]
        if all(s in stats for s in case3):
            return False

        return True

    def check(code: int) -> list:
        lst: list[Status] = []

        for name in Claim.list:
            obj = Claim.list[name]
            if ( (code // obj.value) == 1):
                lst.append(obj)
                code -= obj.value

        return lst
    
    def get(status_list: list) -> int:
        code: int = 0
        
        for stat in status_list:
            code += stat.value
        
        return code