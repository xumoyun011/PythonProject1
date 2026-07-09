def step(u, v, p):
    un = u.clone()
    vn = v.clone()

    # faqat diffuziya + tashqi kuch
    u[1:-1,1:-1] = (
        un[1:-1,1:-1]
        + nu*(dt/dx**2*(un[1:-1,2:]-2*un[1:-1,1:-1]+un[1:-1,0:-2]) +
              dt/dy**2*(un[2:,1:-1]-2*un[1:-1,1:-1]+un[0:-2,1:-1]))
        + F*dt   # 🔥 asosiy haydovchi kuch
    )

    v[1:-1,1:-1] = 0  # kanal oqimida v ≈ 0

    # 🔒 NO-SLIP devorlar
    u[:, 0] = 0
    u[:, -1] = 0
    v[:, 0] = 0
    v[:, -1] = 0

    return u, v, p