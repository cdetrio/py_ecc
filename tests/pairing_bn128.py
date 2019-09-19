import time
from py_ecc import bn128, optimized_bn128

print('Starting bn128 tests pairing_bn128.py')

for lib in (bn128, optimized_bn128):
    print("-----")
    print("doing lib: ", lib)
    FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
    assert FQ(2) * FQ(2) == FQ(4)
    assert FQ(2) / FQ(7) + FQ(9) / FQ(7) == FQ(11) / FQ(7)
    assert FQ(2) * FQ(7) + FQ(9) * FQ(7) == FQ(11) * FQ(7)
    assert FQ(9) ** field_modulus == FQ(9)
    print('FQ works fine')
    
    x = FQ2([1, 0])
    f = FQ2([1, 2])
    fpx = FQ2([2, 2])
    one = FQ2.one()
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    assert x ** (field_modulus ** 2 - 1) == one
    print('FQ2 works fine')
    
    x = FQ12([1] + [0] * 11)
    f = FQ12([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    fpx = FQ12([2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    one = FQ12.one()
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    # This check takes too long
    # assert x ** (field_modulus ** 12 - 1) == one
    print('FQ12 works fine')

    G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply

    assert eq(add(add(double(G1), G1), G1), double(double(G1)))
    assert not eq(double(G1), G1)
    assert eq(add(multiply(G1, 9), multiply(G1, 5)), add(multiply(G1, 12), multiply(G1, 2)))
    assert is_inf(multiply(G1, curve_order))
    print('G1 works fine')

    assert eq(add(add(double(G2), G2), G2), double(double(G2)))
    assert not eq(double(G2), G2)
    assert eq(add(multiply(G2, 9), multiply(G2, 5)), add(multiply(G2, 12), multiply(G2, 2)))
    assert is_inf(multiply(G2, curve_order))
    assert not is_inf(multiply(G2, 2 * field_modulus - curve_order))
    assert is_on_curve(multiply(G2, 9), b2)
    print('G2 works fine')
    
    assert eq(add(add(double(G12), G12), G12), double(double(G12)))
    assert not eq(double(G12), G12)
    assert eq(add(multiply(G12, 9), multiply(G12, 5)), add(multiply(G12, 12), multiply(G12, 2)))
    assert is_on_curve(multiply(G12, 9), b12)
    assert is_inf(multiply(G12, curve_order))
    print('G12 works fine')
    
    pairing, neg = lib.pairing, lib.neg
    
    print("G1 point:", G1)
    print("G2 point:", G2)
    
    """
        // proof_a is a G1 point
        let proof_a = hex::decode("089f41b0e239736338dbacf5893756a5a97ccbacb0f6ba326767b161018a803f26e20505b4f4a99859be674e5fc17025a6b81236302e6c21a59f95e0873b9fa4").unwrap();

        // vk_a is a G2 point
        let vk_a = hex::decode("167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313").unwrap();

        /*
        // from websnark
        const vk_a = [
              //[bigInt("0a6cdc207a41c5e07072ef58074f9cbbacab0c74dcbf2e8594f90db9874e9782",16), bigInt("2c191ae34b6b9b4a8598a7b98c851636a10d4444fea44189f22d894dffae6794", 16)],
              [bigInt("2c191ae34b6b9b4a8598a7b98c851636a10d4444fea44189f22d894dffae6794",16), bigInt("0a6cdc207a41c5e07072ef58074f9cbbacab0c74dcbf2e8594f90db9874e9782", 16)],
              //[bigInt("2ebdd522ff0a7bffbb1e26764cea77cf43c825d18749d421006c7d91da93d25e",16), bigInt("25382aec8d64292e5ab5b95741fe96fca91352d092c983007f7932bb7e79e30c",16)]
              [bigInt("25382aec8d64292e5ab5b95741fe96fca91352d092c983007f7932bb7e79e30c",16), bigInt("2ebdd522ff0a7bffbb1e26764cea77cf43c825d18749d421006c7d91da93d25e",16)]
             ]
        */

        /*
        rs_vk_a_1 = 0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c
        rs_vk_a_2 = 0x24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b
        rs_vk_a_3 = 0x1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d
        rs_vk_a_4 = 0x25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313

        rs_vk_a_1_mont: 0x0a6cdc207a41c5e07072ef58074f9cbbacab0c74dcbf2e8594f90db9874e9782
        rs_vk_a_2_mont: 0x2c191ae34b6b9b4a8598a7b98c851636a10d4444fea44189f22d894dffae6794
        rs_vk_a_3_mont: 0x2ebdd522ff0a7bffbb1e26764cea77cf43c825d18749d421006c7d91da93d25e
        rs_vk_a_4_mont: 0x25382aec8d64292e5ab5b95741fe96fca91352d092c983007f7932bb7e79e30c
        */


        let proof_a_p_x = BigUint::from_str("14567039575197480528119959961327714497845927467213154926371421015062300663263").unwrap();
        let proof_a_p_y = BigUint::from_str("1000373253310235159656639300753059983014930924649970939079246556995097557245").unwrap();

        // neg_a_p is a G1 point
        let neg_a_p = negate(proof_a_p_x, proof_a_p_y);
        println!("negated is {}", hex::encode(&neg_a_p[..]));

        let p2 = hex::decode("198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c21800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa").unwrap();

        let mut output = [0u8; 32];
        let pairing_input = [&proof_a[..], &vk_a[..], &neg_a_p[..], &p2[..]].concat();
    """
    
    #print('Starting pairing tests')
    #a = time.time()
    # g1_point 089f41b0e239736338dbacf5893756a5a97ccbacb0f6ba326767b161018a803f26e20505b4f4a99859be674e5fc17025a6b81236302e6c21a59f95e0873b9fa4
    # 089f41b0e239736338dbacf5893756a5a97ccbacb0f6ba326767b161018a803f
    # 26e20505b4f4a99859be674e5fc17025a6b81236302e6c21a59f95e0873b9fa4
    #
    # G1 = (FQ(1), FQ(2))
    #g1_point = (FQ(0x089f41b0e239736338dbacf5893756a5a97ccbacb0f6ba326767b161018a803f), FQ(0x26e20505b4f4a99859be674e5fc17025a6b81236302e6c21a59f95e0873b9fa4))
    #assert is_on_curve(g1_point, b)
    #print("g1_point is_on_curve IT WORKS!")


    # g1_point = (FQ(0x14507cba49415f9924038310415726d5683a4014fafaf4f6c13ac42f7274c127), FQ(0xa32d771ab825e0def1cb83c706c31631a26bea04ab44b1807dc4ec3fe072b6b))

    # bn128_pairing G1: G1(G1(Fq(2f9691fb0d97c0929d08675020f52d96dce1c62dbae936ca8132bc51fc12af8d), Fq(1e8046402470bf3f64a32cfc8c654c0d975024530193bb17eeda02e3f12d1476), Fq(0e0a77c19a07df2f666ea36f7879462c0a78eb28f5c70b3dd35d438dc58f0d9d)))
    # bn128_pairing G1: G1(G1(Fq(0c0e329b4d73cd52c231f9e064460a7a9f77c7c8752c26efc52e6c7f37d02193), Fq(25f5bae6cf6720e4519b0c6d5b4d6950c116c773a7869909ea0ef64fc73d9ad1), Fq(0e0a77c19a07df2f666ea36f7879462c0a78eb28f5c70b3dd35d438dc58f0d9d)))
    
    # >>> hex(mulmodmont(0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c, 1))
    #'0x55d63b5ba322971b1935b8b82c529377f75f7de2edd169b883a2b2b606d1bbd'

    # >>> hex(mulmodmont(0x2f9691fb0d97c0929d08675020f52d96dce1c62dbae936ca8132bc51fc12af8d, 1))
    # '0x14507cba49415f9924038310415726d5683a4014fafaf4f6c13ac42f7274c127'
    
    # hex(mulmodmont(0x1e8046402470bf3f64a32cfc8c654c0d975024530193bb17eeda02e3f12d1476, 1))
    # '0xa32d771ab825e0def1cb83c706c31631a26bea04ab44b1807dc4ec3fe072b6b'

    # creating G1 from affineG1 a_x: Fq(Fq(2f9691fb0d97c0929d08675020f52d96dce1c62dbae936ca8132bc51fc12af8d)), a_y: Fq(Fq(1e8046402470bf3f64a32cfc8c654c0d975024530193bb17eeda02e3f12d1476))

    # g1_point = (FQ(0x2f9691fb0d97c0929d08675020f52d96dce1c62dbae936ca8132bc51fc12af8d), FQ(0x1e8046402470bf3f64a32cfc8c654c0d975024530193bb17eeda02e3f12d1476), FQ(1))


    #167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313
    # 167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c
    # 24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b
    # 1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d
    # 25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313


    #g2_point = (FQ2([0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c, 0x24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b]),
    #           FQ2([0x1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d, 0x25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313]))


    # G2 = (FQ2([10857046999023057135944570762232829481370756359578518086990519993285655852781, 11559732032986387107991004021392285783925812861821192530917403151452391805634]),
    #      FQ2([8495653923123431417604973247489272438418190587263600148770280649306958101930, 4082367875863433681332203403145435568316851327593401208105741076214120093531]))


    # creating G2 from affineG2 b_a: Fq2(Fq2 { c0: Fq(2c191ae34b6b9b4a8598a7b98c851636a10d4444fea44189f22d894dffae6794), c1: Fq(0a6cdc207a41c5e07072ef58074f9cbbacab0c74dcbf2e8594f90db9874e9782) }),
    # b_b: Fq2(Fq2 { c0: Fq(25382aec8d64292e5ab5b95741fe96fca91352d092c983007f7932bb7e79e30c), c1: Fq(2ebdd522ff0a7bffbb1e26764cea77cf43c825d18749d421006c7d91da93d25e) })

    ## these coords are in montgomery form
    #g2_point = (FQ2([0x2c191ae34b6b9b4a8598a7b98c851636a10d4444fea44189f22d894dffae6794, 0x0a6cdc207a41c5e07072ef58074f9cbbacab0c74dcbf2e8594f90db9874e9782]),
    #            FQ2([0x25382aec8d64292e5ab5b95741fe96fca91352d092c983007f7932bb7e79e30c, 0x2ebdd522ff0a7bffbb1e26764cea77cf43c825d18749d421006c7d91da93d25e]))

    """
        /*
        rs_vk_a_1 = 0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c
        rs_vk_a_2 = 0x24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b
        rs_vk_a_3 = 0x1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d
        rs_vk_a_4 = 0x25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313

        rs_vk_a_1_mont: 0x0a6cdc207a41c5e07072ef58074f9cbbacab0c74dcbf2e8594f90db9874e9782
        rs_vk_a_2_mont: 0x2c191ae34b6b9b4a8598a7b98c851636a10d4444fea44189f22d894dffae6794
        rs_vk_a_3_mont: 0x2ebdd522ff0a7bffbb1e26764cea77cf43c825d18749d421006c7d91da93d25e
        rs_vk_a_4_mont: 0x25382aec8d64292e5ab5b95741fe96fca91352d092c983007f7932bb7e79e30c
        */
    """

    # these are in normal form

    # this one is NOT on G2 curve
    #g2_point = (FQ2([0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c, 0x24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b]),
    #            FQ2([0x1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d, 0x25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313]))


    #g2_point = (FQ2([0x24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b, 0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c]),
    #            FQ2([0x25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313, 0x1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d]))
    #assert is_on_curve(g2_point, b2)
    #print("g2_point is_on_curve YAY!!")

    #test_p1 = pairing(g2_point, g1_point)
    #print("test_p1:", test_p1)

    """
    #p1 = pairing(G2, G1)
    #pn1 = pairing(G2, neg(G1))
    #assert p1 * pn1 == FQ12.one()
    #print('Pairing check against negative in G1 passed')
    #np1 = pairing(neg(G2), G1)
    assert p1 * np1 == FQ12.one()
    assert pn1 == np1
    print('Pairing check against negative in G2 passed')
    assert p1 ** curve_order == FQ12.one()
    print('Pairing output has correct order')
    p2 = pairing(G2, multiply(G1, 2))
    assert p1 * p1 == p2
    print('Pairing bilinearity in G1 passed')
    assert p1 != p2 and p1 != np1 and p2 != np1
    print('Pairing is non-degenerate')
    po2 = pairing(multiply(G2, 2), G1)
    assert p1 * p1 == po2
    print('Pairing bilinearity in G2 passed')
    p3 = pairing(multiply(G2, 27), multiply(G1, 37))
    po3 = pairing(G2, multiply(G1, 999))
    assert p3 == po3
    print('Composite check passed')
    print('Total time for pairings: %.3f' % (time.time() - a))
    """


def test_unoptimized():
    lib = bn128
    FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
    G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply
    pairing, neg = lib.pairing, lib.neg

    print("doing unoptimized bn128 lib...")
    
    # this g1 point is proof_a
    g1_point = (FQ(0x089f41b0e239736338dbacf5893756a5a97ccbacb0f6ba326767b161018a803f), FQ(0x26e20505b4f4a99859be674e5fc17025a6b81236302e6c21a59f95e0873b9fa4))
    assert is_on_curve(g1_point, b)
    print("g1_point is_on_curve IT WORKS!")

    # this g2 point is vk_a
    g2_point = (FQ2([0x24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b, 0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c]),
                FQ2([0x25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313, 0x1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d]))

    assert is_on_curve(g2_point, b2)
    print("g2_point is_on_curve YAY!!")

    test_pairing_result = pairing(g2_point, g1_point)
    #print("test_pairing_result:", as_hex(test_pairing_result))
    print("test_pairing_result:", test_pairing_result)

    """
    let proof_a_p_x = BigUint::from_str("14567039575197480528119959961327714497845927467213154926371421015062300663263").unwrap();
    let proof_a_p_y = BigUint::from_str("1000373253310235159656639300753059983014930924649970939079246556995097557245").unwrap();
    let neg_a_p = negate(proof_a_p_x, proof_a_p_y);

    >>> hex(14567039575197480528119959961327714497845927467213154926371421015062300663263)
    '0x2034a6f7e573a3b1d2c16934721c754bc50fc8c232a4e83c8a7dfa8770311ddf'

    >>> hex(1000373253310235159656639300753059983014930924649970939079246556995097557245)
    '0x23630f23dda7cbc29e510ee9b92e16e16277736a32b01c670bbc77f4c6978fd'
    """

    second_g1_point = (FQ(0x2034a6f7e573a3b1d2c16934721c754bc50fc8c232a4e83c8a7dfa8770311ddf), FQ(0x23630f23dda7cbc29e510ee9b92e16e16277736a32b01c670bbc77f4c6978fd))
    assert is_on_curve(second_g1_point, b)
    print("second_g1_point is_on_curve IT WORKS!")

    """
    let p2 = hex::decode("198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c21800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa").unwrap();
    198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c21800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa

    198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c2
    1800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed
    090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b
    12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa
    """

    second_g2_point = (FQ2([0x1800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed, 0x198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c2]),
                FQ2([0x12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa, 0x090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b]))

    assert is_on_curve(second_g2_point, b2)
    print("second_g2_point is_on_curve YAY!!")

    test_pairing_result_2 = pairing(second_g2_point, neg(second_g1_point))
    print("test_pairing_result_2:", test_pairing_result_2)

    pairing_results_multiplied = test_pairing_result * test_pairing_result_2
    print("pairing_results_multiplied:", pairing_results_multiplied)
    print("FQ12.one():", FQ12.one())
    #assert test_pairing_result * test_pairing_result_2 == FQ12.one()

    return


def test_optimized():
    lib = optimized_bn128
    FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
    G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply
    pairing, neg = lib.pairing, lib.neg

    print("doing optimized_bn128 lib...")

    g1_point = (FQ(0x089f41b0e239736338dbacf5893756a5a97ccbacb0f6ba326767b161018a803f), FQ(0x26e20505b4f4a99859be674e5fc17025a6b81236302e6c21a59f95e0873b9fa4), FQ(1))
    assert is_on_curve(g1_point, b)
    print("g1_point is_on_curve IT WORKS!")

    g2_point = (FQ2([0x24963f8ac35ad1fa13d850fb61eb3c1d2766572452248b14c8e392591b14342b, 0x167595c7e7cd0c935e3a275f254340f7c5a28f5edfa92963a1627e04398fe14c]),
                FQ2([0x25b7f1627599cac3ac91731ff8653662c70afe283da733cd885e12b2be54d313, 0x1a995764699581e0c41626103f9b9a675a503148f4d0b67cbaf1f7ef0b1cc41d]),
                FQ2([1, 0]))

    assert is_on_curve(g2_point, b2)
    print("g2_point is_on_curve YAY!!")
    
    test_pairing_result_optimized = pairing(g2_point, g1_point)
    print("test_pairing_result_optimized:", test_pairing_result_optimized)

    return


test_unoptimized()
test_optimized()

