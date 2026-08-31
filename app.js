/* ============================================================
   BRI — hero animation: rotating Earth, satellites, clock ring
   ------------------------------------------------------------
   The settings you are most likely to change are at the top.
   ============================================================ */
(function () {
  "use strict";

  /* ---------- SETTINGS ---------- */

  // Cities in the orbiting clock ring. Add or remove lines freely.
  // Time zone names come from the standard IANA time zone list.
  var CITIES = [
    { name: "New York",      tz: "America/New_York"    },
    { name: "San Francisco", tz: "America/Los_Angeles" },
    { name: "London",        tz: "Europe/London"       },
    { name: "Hamburg",       tz: "Europe/Berlin"       },
    { name: "Hong Kong",     tz: "Asia/Hong_Kong"      },
    { name: "Beijing",       tz: "Asia/Shanghai"       },
    { name: "Tokyo",         tz: "Asia/Tokyo"          },
    { name: "Melbourne",     tz: "Australia/Melbourne" }
  ];

  var GLOBE_SPIN_SECONDS  = 45;   // seconds for one full turn of the Earth
  var CLOCK_ORBIT_SECONDS = 160;  // seconds for one full lap of the clock ring
  var MOBILE_BREAKPOINT   = 720;  // below this width, clocks become a plain grid

  // Satellites: distance (multiples of globe radius), tilt, roll, lap time, colour
  var SATELLITES = [
    { dist: 1.30, tilt: 74, roll:  18, seconds: 15, color: "#00d4ff" },
    { dist: 1.62, tilt: 58, roll: -32, seconds: 26, color: "#a855f7" },
    { dist: 1.12, tilt: 86, roll:  58, seconds: 11, color: "#7bffcd" }
  ];

  /* ---------- LANDMASS MAP ----------
     Rough continent boxes as [westLon, southLat, eastLon, northLat].
     These get sampled into dots, so precision is not important. */
  var LAND = [
    [-168,54,-141,72], [-141,50,-62,72], [-127,32,-70,50], [-115,15,-88,32], [-92,7,-77,18],
    [-52,60,-22,82],
    [-79,-4,-35,12], [-77,-24,-38,-4], [-72,-40,-50,-24], [-73,-54,-64,-40],
    [-9,36,28,55], [4,55,31,70], [-9,50,1,58],
    [-17,8,32,33], [8,-4,42,8], [11,-17,40,-4], [15,-34,33,-17], [43,-25,50,-12],
    [34,12,58,32], [28,42,58,70], [58,50,180,74], [55,28,90,50], [68,8,88,28],
    [95,22,134,48], [129,32,145,45], [96,6,109,22], [118,5,126,19],
    [95,-9,140,5], [113,-38,153,-12], [166,-46,178,-35],
    [-180,-90,180,-64]
  ];

  var D2R = Math.PI / 180;

  function isLand(lon, lat) {
    for (var i = 0; i < LAND.length; i++) {
      var r = LAND[i];
      if (lon >= r[0] && lon <= r[2] && lat >= r[1] && lat <= r[3]) return true;
    }
    return false;
  }

  // Stable pseudo-random so the dot pattern looks organic but never flickers.
  function noise(a, b) {
    var s = Math.sin(a * 127.1 + b * 311.7) * 43758.5453;
    return s - Math.floor(s);
  }

  // Build the land dots once, spaced evenly over the sphere.
  var DOTS = [];
  (function buildDots() {
    var step = 3;
    for (var lat = -87; lat <= 87; lat += step) {
      var lonStep = step / Math.max(0.22, Math.cos(lat * D2R));
      for (var lon = -180; lon < 180; lon += lonStep) {
        if (!isLand(lon, lat)) continue;
        if (noise(lon, lat) < 0.16) continue;
        DOTS.push([lon * D2R, lat * D2R]);
      }
    }
  })();

  /* ---------- SETUP ---------- */
  var canvas = document.getElementById("globe");
  var layer  = document.getElementById("clockLayer");
  if (!canvas || !layer) return;
  var ctx = canvas.getContext("2d");

  var nodes = [];
  var formatters = [];
  CITIES.forEach(function (city) {
    formatters.push(new Intl.DateTimeFormat("en-US", {
      timeZone: city.tz, hour: "numeric", minute: "2-digit", hour12: true
    }));
    var node = document.createElement("div");
    node.className = "clock-node";
    node.innerHTML = '<div class="clock-card">' +
      '<div class="clock-time">--:--</div>' +
      '<div class="clock-city">' + city.name + '</div></div>';
    layer.appendChild(node);
    nodes.push(node);
  });

  function updateTimes() {
    var now = new Date();
    for (var i = 0; i < nodes.length; i++) {
      var t = formatters[i].format(now).toLowerCase().replace(/[\s\u202f\u00a0]/g, "");
      nodes[i].firstChild.firstChild.textContent = t;
    }
  }
  updateTimes();
  setInterval(updateTimes, 1000);

  var W = 0, H = 0, dpr = 1;
  function resize() {
    var rect = canvas.getBoundingClientRect();
    W = rect.width; H = rect.height;
    dpr = window.devicePixelRatio || 1;
    canvas.width  = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener("resize", resize);
  resize();

  /* ---------- 3D HELPERS ---------- */
  function project(lonRad, latRad, spin, cx, cy, R) {
    var lo = lonRad + spin;
    var cl = Math.cos(latRad);
    return {
      x: cx + cl * Math.sin(lo) * R,
      y: cy - Math.sin(latRad) * R,
      z: cl * Math.cos(lo)
    };
  }

  function satPoint(sat, angle, cx, cy, R) {
    var r = R * sat.dist;
    var x = Math.cos(angle) * r, y = Math.sin(angle) * r, z = 0;
    var tx = sat.tilt * D2R;
    var y2 = y * Math.cos(tx) - z * Math.sin(tx);
    var z2 = y * Math.sin(tx) + z * Math.cos(tx);
    var rz = sat.roll * D2R;
    return {
      x: cx + (x * Math.cos(rz) - y2 * Math.sin(rz)),
      y: cy - (x * Math.sin(rz) + y2 * Math.cos(rz)),
      z: z2
    };
  }

  function drawOrbitPath(sat, cx, cy, R, wantFront) {
    ctx.beginPath();
    var drawing = false;
    for (var i = 0; i <= 180; i++) {
      var p = satPoint(sat, (i / 180) * Math.PI * 2, cx, cy, R);
      if ((p.z > 0) === wantFront) {
        if (drawing) ctx.lineTo(p.x, p.y);
        else { ctx.moveTo(p.x, p.y); drawing = true; }
      } else drawing = false;
    }
    ctx.strokeStyle = wantFront ? "rgba(0,212,255,0.22)" : "rgba(0,212,255,0.09)";
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  function drawSatellite(p, sat, R) {
    var s = 0.7 + 0.5 * (p.z / (R * sat.dist) + 1) / 2;
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.shadowBlur = 12;
    ctx.shadowColor = sat.color;
    ctx.fillStyle = sat.color;
    ctx.fillRect(-2.2 * s, -2.2 * s, 4.4 * s, 4.4 * s);
    ctx.fillRect(-7.5 * s, -1.1 * s, 4.2 * s, 2.2 * s);
    ctx.fillRect(3.3 * s,  -1.1 * s, 4.2 * s, 2.2 * s);
    ctx.restore();
  }

  function drawGlobe(spin, cx, cy, R) {
    // atmosphere halo
    var halo = ctx.createRadialGradient(cx, cy, R * 0.95, cx, cy, R * 1.32);
    halo.addColorStop(0, "rgba(0,175,255,0.30)");
    halo.addColorStop(1, "rgba(0,140,255,0)");
    ctx.fillStyle = halo;
    ctx.beginPath(); ctx.arc(cx, cy, R * 1.32, 0, Math.PI * 2); ctx.fill();

    ctx.save();
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.clip();

    // ocean
    var sea = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.08, cx, cy, R);
    sea.addColorStop(0, "#1d5596");
    sea.addColorStop(0.55, "#0d2b57");
    sea.addColorStop(1, "#04122b");
    ctx.fillStyle = sea;
    ctx.fillRect(cx - R, cy - R, R * 2, R * 2);

    // graticule
    ctx.strokeStyle = "rgba(120,200,255,0.13)";
    ctx.lineWidth = 0.7;
    var lat, lon, i, p, started;
    for (lat = -60; lat <= 60; lat += 30) {
      ctx.beginPath(); started = false;
      for (i = 0; i <= 120; i++) {
        p = project((-180 + i * 3) * D2R, lat * D2R, spin, cx, cy, R);
        if (p.z > 0) { started ? ctx.lineTo(p.x, p.y) : (ctx.moveTo(p.x, p.y), started = true); }
        else started = false;
      }
      ctx.stroke();
    }
    for (lon = -180; lon < 180; lon += 30) {
      ctx.beginPath(); started = false;
      for (i = 0; i <= 90; i++) {
        p = project(lon * D2R, (-90 + i * 2) * D2R, spin, cx, cy, R);
        if (p.z > 0) { started ? ctx.lineTo(p.x, p.y) : (ctx.moveTo(p.x, p.y), started = true); }
        else started = false;
      }
      ctx.stroke();
    }

    // land dots
    for (i = 0; i < DOTS.length; i++) {
      p = project(DOTS[i][0], DOTS[i][1], spin, cx, cy, R);
      if (p.z <= 0.02) continue;
      var size = (0.75 + 1.15 * p.z) * (R / 120);
      ctx.fillStyle = "rgba(112,240,205," + (0.22 + 0.72 * p.z) + ")";
      ctx.fillRect(p.x - size / 2, p.y - size / 2, size, size);
    }

    // sphere shading
    var shade = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.35, R * 0.05, cx, cy, R * 1.02);
    shade.addColorStop(0, "rgba(255,255,255,0.10)");
    shade.addColorStop(0.5, "rgba(0,0,0,0)");
    shade.addColorStop(1, "rgba(0,4,26,0.60)");
    ctx.fillStyle = shade;
    ctx.fillRect(cx - R, cy - R, R * 2, R * 2);
    ctx.restore();

    // rim light
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.strokeStyle = "rgba(0,212,255,0.45)";
    ctx.lineWidth = 1.1;
    ctx.stroke();
  }

  /* ---------- MAIN LOOP ---------- */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function frame(ms) {
    var t = reduceMotion ? 8000 : ms;
    var cx = W / 2, cy = H / 2;
    var R = Math.min(W, H) * 0.21;
    var spin = (t / 1000) * (Math.PI * 2 / GLOBE_SPIN_SECONDS);

    ctx.clearRect(0, 0, W, H);

    var i, sat, p, pts = [];
    for (i = 0; i < SATELLITES.length; i++) {
      sat = SATELLITES[i];
      p = satPoint(sat, (t / 1000) * (Math.PI * 2 / sat.seconds), cx, cy, R);
      pts.push(p);
      drawOrbitPath(sat, cx, cy, R, false);
      if (p.z <= 0) drawSatellite(p, sat, R);
    }

    drawGlobe(spin, cx, cy, R);

    for (i = 0; i < SATELLITES.length; i++) {
      drawOrbitPath(SATELLITES[i], cx, cy, R, true);
      if (pts[i].z > 0) drawSatellite(pts[i], SATELLITES[i], R);
    }

    // move the clocks around their ring
    if (window.innerWidth > MOBILE_BREAKPOINT) {
      var rx = Math.min(W / 2 - 64, 340);
      var ry = Math.min(H / 2 - 28, 248);
      var base = (t / 1000) * (Math.PI * 2 / CLOCK_ORBIT_SECONDS);
      for (i = 0; i < nodes.length; i++) {
        var a = base + i * (Math.PI * 2 / nodes.length);
        var scale = 0.88 + 0.12 * (1 - Math.cos(a)) / 2;
        nodes[i].style.transform =
          "translate(" + (cx + Math.sin(a) * rx) + "px," + (cy - Math.cos(a) * ry) + "px)" +
          " translate(-50%,-50%) scale(" + scale.toFixed(3) + ")";
      }
    }

    if (!reduceMotion) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
