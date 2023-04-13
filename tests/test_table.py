import clitable.table as table


def test_get_headers():
    # Arrange
    headers = ["header1", "header2"]
    dut = table.Table(headers)

    # Act
    ret = dut.get_headers()

    # Assert
    assert len(ret) == 2
    assert ret[0] == "header1"
    assert ret[1] == "header2"

def test_iterator():
    # Arrange
    headers = ["header1", "header2"]
    data = [[1, 2], [3,4]]

    dut = table.Table(headers, data = data)
    
    # Act
    ret = [i for i in dut]

    # Assert
    assert len(ret) == 2
    assert len(ret[0]) == 2
    assert ret[0][0] == 1
    assert ret[0][1] == 2
    assert len(ret[1]) == 2
    assert ret[1][0] == 3
    assert ret[1][1] == 4