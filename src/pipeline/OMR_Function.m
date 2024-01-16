
function out = OMR_Function(a, QQQ)
    M = readmatrix(a);
    [rr, cc] = size(M);
    M = M(2:end, 2:end);
    [row, col] = find(M < log(0.5));
    count = 1;
    sink = [0, 0, 0];
    storeXY = cell(1);
    for i = 1:length(row)
        val = M(row(i), col(i));
        r = true;
        y = row(i);
        x = col(i);
        x1 = -100;
        y1 = - 100;
        store = [-100, -100];
        q = 1;
        while dist(x, y, x1, y1) > 0.5 && r
            d(1, 1) = (M(max(y - 1, 1), max(x-1, 1))- val)/sqrt(2);
            d(1, 2) = M(y, max(x-1, 1))- val;
            d(1, 3) = (M(min(y + 1, rr), max(x-1, 1)) - val)/sqrt(2);
            d(1, 4) = M(max(y - 1, 1), x) - val;
            d(1, 5) = M(min(y + 1, rr), x) - val;
            d(1, 6) = (M(min(y + 1, rr), min(x+1, cc))- val)/sqrt(2);
            d(1, 7) = M(y, min(x+1, cc))- val;
            d(1, 8) = (M(max(y - 1, 1), min(x+1, cc))- val)/sqrt(2);
            d(1, 9) = 0;
            [S, I] = min(d);
            I = I(1);
            x1 = x;
            y1 = y;

            for w = 1:q
                if dist(x, y, store(w, 1), store(w, 2)) < 0.5
                    r = false;
                end
            end
            q = q + 1;
            store(q, :) = [x, y];
            g = choose(I, x, y, rr, cc);
            y = g(1);
            x = g(2);
            val = M(y, x);
        end
        store = store(2:end, :);
        tu = true;
        SS = size(sink);
        SS = SS(1);
        for e = 1:SS
            if dist(x, y, sink(e, 2), sink(e, 1)) < 10
                sink(e, 3) = sink(e, 3) + 1;
                storeXY{e} = [storeXY{e};store];
                tu = false;
                break;
            end
        end
        if tu 
            sink(count, 1:3) = [y, x, 1];
            storeXY{count} = store;
            count = count + 1;  
        end
    end
    k = 1;
    for i = 1:count-1
        Q = storeXY{i};
        if length(Q) > 100
            %plot(Q(:, 1), -Q(:, 2), 'o', 'Color', rand(1, 3));
            %hold on;
            meanPos(1, k) = mean(Q(:, 1));
            meanPos(2, k) = mean(Q(:, 2));
            %plot(meanPos(1, k), -meanPos(2, k), 'o', 'MarkerSize', 10, 'Color', 'r');
            k = k + 1;
        end
    end
    try
        A = sprintf('notes_position%d.csv', QQQ);
        writematrix(meanPos.', A);
        out = 1;
    catch 
        out = 0;
    end
end



function out = choose(p, kx, ky, rr, cc)
    if p == 1
        out = [max(ky - 1, 1), max(kx - 1, 1)];
    elseif p == 2
        out = [ky, max(kx - 1, 1)];
    elseif p == 3
        out = [min(ky + 1, rr), max(kx - 1, 1)];
    elseif p == 4
        out = [max(ky - 1, 1), kx];
    elseif p == 5
        out = [min(ky + 1, rr), kx];
    elseif p == 6
        out = [min(ky + 1, rr), min(kx + 1, cc)];
    elseif p == 7
        out = [ky, min(kx + 1, cc)];
    elseif p == 8
        out = [max(ky - 1, 1), min(kx + 1, cc)];
    else
        out = [ky, kx];
    end
end

function out = dist(x, y, x1, y1) 

    out = sqrt((x - x1)^2 + (y - y1)^2);
end
