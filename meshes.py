class Cube:
   corners = (
      # Back face
      (0, 0, 0),
      (0, 1, 0),
      (1, 1, 0),
      (1, 0, 0),

      # Front face
      (0, 0, 1),
      (0, 1, 1),
      (1, 1, 1),
      (1, 0, 1),
   )

   rawVertices = (
      corners[0],
      corners[1],
      corners[2],
      corners[3],

      corners[4],
      corners[5],
      corners[6],
      corners[7]
   )